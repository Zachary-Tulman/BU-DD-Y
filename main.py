from buddy import Buddy
import argparse

parser = argparse.ArgumentParser(description="Voice Assistant")
parser.add_argument("--devices", action="store_true",
                    help="List available audio devices and exit")
parser.add_argument("--voices", action="store_true",
                    help="List available TTS voices and exit")

args = parser.parse_args()

if args.devices:
    from audio import text_to_speech as tts
    # empty object is passed because we aren't initializing
    text_to_speech = tts.TextToSpeech({})
    # TODO: if we are sticking with pyaudio, write a loop to list all device info
    #       if we are moving to sounddevice, it's a little easier
    print(text_to_speech.p.get_device_info_by_index(0))

# TODO: Decide if we are sticking with pyaudio or switching to sounddevice.
#       It all hinges on if we can still do the audio stream onto the jabra with sounddevice




# TODO: modify build to be OS-agnostic for dev/prod release split (testing on linux platforms)

# TODO: add "transcription" mode where buddy just takes all the text it recognizes until it hears a key word then spits out the end result

# TODO: "save messages", "how many?", save w/e number is given

# TODO: Implement search.
#   When phrase "search" is detected in message, call ChatGPT API for real search function
if __name__ == "__main__":
    buddy = Buddy()
    buddy.run()