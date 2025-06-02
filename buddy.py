from audio import text_to_speech as tts, speech_recognition as sr
from models import deepseek as LangModel
from utils import message_handler as MsgUtils
from config import load_config

class Buddy:
    def __init__(self):
        config = load_config()
        self.config = {
            "SPEAKER_NAME": config.get("SPEAKER_NAME"),
            "MICROPHONE_NAME": config.get("MICROPHONE_NAME")
        }

        self.model = LangModel.DeepSeekModel({"DEEPSEEK_API_KEY": config.get("DEEPSEEK_API_KEY")})
        self.model.init_with_prompt(config.get("BUDDY_PROMPT"))

        self.sr = sr.SpeechRecognition(self.config)
        self.tts = tts.TextToSpeech(self.config)
        self.msg_utils = MsgUtils.MessageHandler()

        self.standby = True

        self._initialize()

    def _initialize(self):
        self.tts.initialize()

        self.tts.speak("I am calibrating audio... Please be silent for about 3 seconds...")
        self.sr.initialize()
        self.tts.speak("Calibration complete. How may I help you today?")
    
    def run(self):
        while True:
            if self.standby == False:
                self.tts.play_ready_tone()

            text = self.sr.record_input()
            print(f"Interpreted text: {text}")
            
            # move these checks to a switch statement in a different function or something
            # i feel like that should be most optimal even though i'm doing separate functions for now
            if self.msg_utils.check_end_of_line(text):
                if self.standby == False:
                    self.tts.play_ready_tone(frequency=440)
                    print("Entering standby mode.")
                    self.tts.speak("Okay. Entering standby mode.")
                self.standby = True
                continue

            if self.standby == True and not self.msg_utils.check_hey_buddy(text):
                continue

            if self.msg_utils.check_mark_last_message(text):
                print("Okay! Last message has been marked.")
                self.tts.speak("Okay! Last message has been marked.")
                continue

            if self.msg_utils.check_save_marked_messages(text):
                print("Saving to disk...")
                self.msg_utils.save_marked_messages()

                print("Okay! Marked messages have been saved to an html file.")
                self.tts.speak("Okay! Marked messages have been saved to an html file.")
                continue

            self.standby = False
            self.tts.play_ready_tone(frequency=440)
            response_stream = self.model.send_message(text)
            full_response = self.tts.process_streamed_response(response_stream)

            # we may also want streamed printing instead of all at once after it's been spoken
            print(full_response)

            self.model.append_assistant_response(full_response)