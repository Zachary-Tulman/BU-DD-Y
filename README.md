# BU-DD-Y

BU-DD-Y (pronounced "Buddy") is a voice-activated AI chat assistant that you can converse with in real time.

### How it works
BU-DD-Y operates on a basic loop:
1) Vosk speech recognition is used to locally convert user voice input to a string of legible text.
2) The converted text is sent through an LLM API of choice.
3) The API response is separated into sentence-boundary chunks as it is streamed back.
4) The streamed response chunks are spoken via pyttsx3 text-to-speech as they are received to minimize perceived latency.
5) When the response is complete, the bot waits back at step 1 for more user voice input.

## Features
- Wake word activation ("hey buddy") with standby mode. Say "end of line" to return to standby
- Tone audio feedback on state changes
- Mark and save assistant responses to formatted HTML files
- Configurable microphone, speaker, and voice selection
- Ambient noise calibration on startup

### Tech Stack
Python, Vosk, SpeechRecognition, pyttsx3, PyAudio, OpenAI SDK, python-dotenv
