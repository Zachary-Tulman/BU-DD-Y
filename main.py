from buddy import Buddy
import argparse

parser = argparse.ArgumentParser(description="Voice Assistant")
parser.add_argument("--devices", action="store_true",
                    help="List available audio devices and exit")
parser.add_argument("--voices", action="store_true",
                    help="List available TTS voices and exit")

args = parser.parse_args()

if args.devices:
    import sounddevice as sd
    print(sd.query_devices())

if args.voices:
    import pyttsx3
    engine = pyttsx3.init()
    voices = engine.getProperty("voices")
    for voice in voices:
        print(voice.name)


# TODO: modify build to be OS-agnostic for dev/prod release split (testing on linux platforms)
#   - create "requirements.txt"
#   - upload to a private github repo
#   - clone to linux, install requirements.txt idk how to do that
#   - run in linux (should need to install espeak and something else that i forgot)
#   - once you know what to install, find out how to check for its absence and put a message saying how to download it


# TODO: add "transcription" mode where buddy just takes all the text it recognizes until it hears a key word then spits out the end result

# TODO: "save messages", "how many?", save w/e number is given

# TODO: Implement search.
#   When phrase "search" is detected in message, call ChatGPT API for real search function
if __name__ == "__main__":
    buddy = Buddy()
    buddy.run()