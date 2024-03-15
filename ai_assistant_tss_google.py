import pygame
import time
import speech_recognition as sr
import whisper
import queue
import os
import threading
import torch
import numpy as np
import re
from openai import OpenAI
import click
from dotenv import load_dotenv
import os
from google.cloud import texttospeech

google_client = texttospeech.TextToSpeechClient()

load_dotenv() 
client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
)

@click.command()
@click.option("--model", default="base", help="Model to use", type=click.Choice(["tiny", "base", "small", "medium", "large"]))
@click.option("--english", default=False, help="Whether to use the English model", is_flag=True, type=bool)
@click.option("--energy", default=300, help="Energy level for the mic to detect", type=int)
@click.option("--pause", default=0.8, help="Pause time before entry ends", type=float)
@click.option("--dynamic_energy", default=False, is_flag=True, help="Flag to enable dynamic energy", type=bool)
@click.option("--wake_word", default="hey computer", help="Wake word to listen for", type=str)
@click.option("--verbose", default=False, help="Whether to print verbose output", is_flag=True, type=bool)

def main(model, english, energy, pause, dynamic_energy, wake_word, verbose):
    if model != "large" and english:
        model = model + ".en"
    audio_model = whisper.load_model(model)
    audio_queue = queue.Queue()
    result_queue = queue.Queue()

    threading.Thread(target=record_audio, args=(audio_queue, energy, pause, dynamic_energy,)).start()
    threading.Thread(target=transcribe_forever, args=(audio_queue, result_queue, audio_model, english, wake_word, verbose,)).start()
    threading.Thread(target=reply, args=(result_queue,)).start()

    while True:
        print(result_queue.get())

def record_audio(audio_queue, energy, pause, dynamic_energy):
    r = sr.Recognizer()
    r.energy_threshold = energy
    r.pause_threshold = pause
    r.dynamic_energy_threshold = dynamic_energy

    with sr.Microphone(sample_rate=16000) as source:
        print("Listening...")
        i = 0
        while True:
            audio = r.listen(source)
            torch_audio = torch.from_numpy(np.frombuffer(audio.get_raw_data(), np.int16).flatten().astype(np.float32) / 32768.0)
            audio_data = torch_audio
            audio_queue.put_nowait(audio_data)
            i += 1

def transcribe_forever(audio_queue, result_queue, audio_model, english, wake_word, verbose):
    while True:
        audio_data = audio_queue.get()
        if english:
            result = audio_model.transcribe(audio_data, language='english')
        else:
            result = audio_model.transcribe(audio_data)

        predicted_text = result["text"]

        if predicted_text.strip().lower().startswith(wake_word.strip().lower()):
            pattern = re.compile(re.escape(wake_word), re.IGNORECASE)
            predicted_text = pattern.sub("", predicted_text).strip()
            punc = '''!()-[]{};:'"\,<>./?@#$%^&*_~'''
            predicted_text = predicted_text.translate({ord(i): None for i in punc})
            if verbose:
                print("You said the wake word.. Processing {}...".format(predicted_text))

            result_queue.put_nowait(predicted_text)
        else:
            if verbose:
                print("You did not say the wake word.. Ignoring")

        if not predicted_text:
            if verbose:
                print("No text recognized from the audio input.")
            continue

def get_completion_from_messages(messages, model="gpt-3.5-turbo", temperature=0.4, max_tokens=500):
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=temperature,
        max_tokens=max_tokens,
    )
    if response.choices and len(response.choices) > 0:
        last_message = response.choices[-1].message
        last_message_content = last_message.content
        return last_message_content
    else:
        return "No response generated."

def reply(result_queue):
    while True:
        result = result_queue.get()

        if not result:
            print("No result to process.")
            continue

        messages = [{"role": "user", "content": result}] if result else []
        
        if messages:
            answer = get_completion_from_messages(messages)
            synthesis_input = texttospeech.SynthesisInput(text=answer)
            voice = texttospeech.VoiceSelectionParams(language_code="en-US", ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL)
            audio_config = texttospeech.AudioConfig(audio_encoding=texttospeech.AudioEncoding.MP3)
            response = google_client.synthesize_speech(input=synthesis_input, voice=voice, audio_config=audio_config)
            with open("output.mp3", "wb") as out:
                out.write(response.audio_content)
                print('Audio content written to file "output.mp3"')
            pygame.mixer.init()
            sound = pygame.mixer.Sound("output.mp3")
            sound.play()
            time.sleep(sound.get_length())
        else:
            print("Empty message list, skipping API call.")

if __name__ == "__main__":
    main()

