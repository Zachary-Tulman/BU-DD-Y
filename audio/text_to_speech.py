import pyttsx3
import pyaudio
import wave
import tempfile
import os
import time
import numpy as np
import re
import sys

class TextToSpeech:
    def __init__(self, config):
        self.config = config
        self.engine = pyttsx3.init()
        self.p = pyaudio.PyAudio()
        self.speaker_index = None
    
    def initialize(self):
        voices = self.engine.getProperty("voices")
        self.engine.setProperty("voice", voices[self.config.get("VOICE_INDEX")].id)
        self.engine.setProperty("rate", 140)

        self.speaker_index = self._get_speaker_index()

    def _get_speaker_index(self):
        for i in range(self.p.get_device_count()):
            if self.config.get("SPEAKER_NAME") in self.p.get_device_info_by_index(i)['name']:
                return i
        return self.p.get_default_output_device_info()['index']

    def speak(self, text):
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmpfile:
            wav_path = tmpfile.name
        
        self.engine.save_to_file(f"<pitch middle='-1'>{text}</pitch>", wav_path)
        self.engine.runAndWait()

        wf = wave.open(wav_path, 'rb')
        
        stream = self.p.open(format=self.p.get_format_from_width(wf.getsampwidth()),
            channels = wf.getnchannels(),
            rate=wf.getframerate(),
            output=True,
            output_device_index=self._get_speaker_index())
        
        data = wf.readframes(1024)
        while data:
            stream.write(data)
            data = wf.readframes(1024)
        
        stream.stop_stream()
        stream.close()
        wf.close()

        os.unlink(wav_path)

    def process_streamed_response(self, response) -> str:
        full_response = ""
        buffer = ""

        for chunk in response:
            if chunk.choices[0].delta.content is not None:
                chunk_content = chunk.choices[0].delta.content
                full_response += chunk_content
                buffer += chunk_content

                if re.search(r'[.!?]\s|[:;,]\s|\n', buffer):
                    sentences = re.split(r'([.!?]\s|[;:,]\s|\n)', buffer)
                    speak_text = ""
                    keep_text = ""

                    for i in range(0, len(sentences)-1, 2):
                        speak_text += sentences[i] + sentences[i+1]

                    if len(sentences) % 2 == 1:
                        keep_text = sentences[-1]

                    if speak_text:
                        self.speak(speak_text)
                    
                    buffer = keep_text
        
        if buffer.strip():
            self.speak(buffer)

        return full_response

    def play_tone(self, frequency=880, duration=0.2):
        sample_rate = 44100 # Sound quality (higher = better)
        amplitude = 0.3     # Volume (0.0 to 1.0)

        # create generic tone data
        num_samples = int(sample_rate * duration)
        t = np.linspace(0, duration, num_samples, False)
        decay = np.exp(-t * 8)  # 8 is random, higher = faster decay
        tone_data = amplitude * np.sin(2 * np.pi * frequency * t) * decay

        # convert audio_data to 16 bit format used by pyaudio
        # 32767 == 2^15 - 1
        audio_data = (tone_data * 32767).astype(np.int16).tobytes()

        stream = self.p.open(
            format=self.p.get_format_from_width(2),
            channels=1,
            rate=sample_rate,
            output=True,
            output_device_index=self._get_speaker_index()
        )

        stream.write(audio_data)

        stream.stop_stream()
        stream.close()

        time.sleep(0.1)