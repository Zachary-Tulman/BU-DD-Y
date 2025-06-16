import os
from dotenv import load_dotenv

def load_config():
    load_dotenv()

    ### Peripheral names are string-matched. You can find a full list of your
    #       device's peripheral names by running "py main.py --devices"
    return {
        "DEEPSEEK_API_KEY": os.getenv("DEEPSEEK_API_KEY"),
        "BUDDY_PROMPT": os.getenv("BUDDY_PROMPT"),
        "SPEAKER_NAME": os.getenv("SPEAKER_NAME"),
        "VOICE_INDEX": int(os.getenv("VOICE_INDEX", 0)),
        "MICROPHONE_NAME": os.getenv("MICROPHONE_NAME"),
    }