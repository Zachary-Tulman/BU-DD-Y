import speech_recognition as sr
import json
import os

class SpeechRecognition:
    def __init__(self, config):
        self.config = config
        self.r = sr.Recognizer()
        self.mic_index = None
    
    def initialize(self):
        self.r.energy_threshold = 700
        self.r.pause_threshold = 1.25
        self.r.dynamic_energy_threshold = False

        self.mic_index = self._get_mic_index()

        self.calibrate_audio()

    def calibrate_audio(self):
        with sr.Microphone(device_index=self._get_mic_index()) as mic_source:
            self.r.adjust_for_ambient_noise(mic_source)

            dummy_audio = self.r.record(mic_source, duration=0.1)
            try:
                self.r.recognize_vosk(dummy_audio)
            except sr.UnknownValueError:
                pass

    def _get_mic_index(self):
        mic_names = sr.Microphone.list_microphone_names()
        return next((i for i, s in enumerate(mic_names) if os.getenv("MICROPHONE_NAME") in s))
    
    def record_input(self) -> str:
        while True:
            try:
                with sr.Microphone(device_index=self._get_mic_index()) as mic_source:
                    print("Accepting voice input. Please speak...")
                    raw_audio = self.r.listen(
                        mic_source,
                    )
                    print("Processing...")
                    r_json = self.r.recognize_vosk(raw_audio)
                    r_dict = json.loads(r_json)
                    if "text" in r_dict:
                        r_text = r_dict["text"].strip()
                        # Vosk often misinterprets silence as the word "the"
                        if r_text and r_text != "the":
                            return r_text
                        else:
                            print("Ignoring non-speech audio...")
                    else:
                        print("No text recognized.")
            
            except sr.RequestError as e:
                print("The recognizer encountered an error; {0}".format(e))
            
            except sr.UnknownValueError:
                print("Audio input could not be resolved.")

            except json.JSONDecodeError:
                print("There was an error decoding microphone input.")