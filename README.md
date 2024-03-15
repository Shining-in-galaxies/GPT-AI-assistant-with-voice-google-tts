# GPT-AI-assistant-with-voice

Real time tts AI assistant chatbot powered by GPT, Siri & Alexa like

## Introduction

This repository hosts an innovative real-time, voice-activated AI assistant akin to Siri and Alexa. It's built using Python and leverages technologies like OpenAI's API, Whisper for voice recognition, and gTTS for dynamic text-to-speech responses, offering users a seamless interactive experience.

## Presentation

View presentation [PDF file](https://drive.google.com/file/d/1D70OZN7h9z6tpeVjsL__bYc_t98NdsgN/view?usp=share_link)

## Features

- Real-time voice to text conversion with `speech_recognition` and `whisper`.
- Lifelike text-to-speech responses using OpenAI models.
- Customizable wake word and adjustable microphone sensitivity.
- Flexible model selection for optimal performance.
- Cross-platform support and verbose debugging mode.

## Tech Stack

- **Python**: Core programming language.
- **OpenAI API**: Natural language processing and generation.
- **Whisper**: Speech recognition.
- **Google TTS**: Text-to-speech conversion.
- **Pydub**: Audio manipulation.
- **Threading & Queue**: Concurrent execution and inter-thread communication.

## Environment

Developed and tested for Linux.

## Installation and Setup

1. Check Python Version
   Ensure you have Python 3 installed by running:
   `python3 --version`
   If Python is not installed, follow the instructions here: [Install Python on Ubuntu](https://www.makeuseof.com/install-python-ubuntu/).

2. Update your package list and install pip:
   `sudo apt update`
   `sudo apt install python3-pip`

3. Install virtual environment tools:
   `sudo apt install virtualenv virtualenvwrapper`

4. Configure the virtual environment:

   - Open file:
     `nano ~/.bashrc`
   - Add the following lines to the end of the file:
     `WORKON_HOME=$HOME/.virtualenvs`
     `VIRTUAL_ENVWRAPPER_PYTHON=/usr/bin/python3`
     `source /usr/share/virtualenvwrapper/virtualenvwrapper.sh`

5. Create a new virtual environment:
   `mkvirtualenv example`

6. Work on virtual environment:
   `workon example`

7. Clone this repository.

8. Navigate into the project directory:
   `cd ai-ecommerce-email-assistant`

9. Install the requirements:
   `pip install -r requirements.txt`

10. [OpenAI Migration](https://github.com/openai/openai-python/discussions/742):
    `openai migrate`

11. [Get your API key](https://beta.openai.com/account/api-keys)

12. Add OpenAI API Key to the Virtual Environment`s Environment Variables

    - Open or create an .env file within your virtual environment:
      `nano .env`
    - In the .env file, enter the following line, replacing your_api_key_here with your actual OpenAI API key:
      `OPENAI_API_KEY=your_api_key_here`
    - Activate the environment variables in your current session:
      `source .env`
    - Test if the OpenAI API Key was successfully added by printing it:
      `echo $OPENAI_API_KEY`
      If the command prints your API key, it has been successfully added to the environment variables.

13. Running the Application
    `python3 ai_assistant_tss.py`
    At this point, you can talk through microphone starting with `hey computer` to chat with the AI assistant.
