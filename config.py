import os
from dotenv import load_dotenv

def load_config():
    load_dotenv()

    return {
        "DEEPSEEK_API_KEY": os.getenv("DEEPSEEK_API_KEY"),
        "BUDDY_PROMPT": os.getenv("BUDDY_PROMPT"),
        "SPEAKER_NAME": os.getenv("SPEAKER_NAME"),
        "MICROPHONE_NAME": os.getenv("MICROPHONE_NAME")
    }