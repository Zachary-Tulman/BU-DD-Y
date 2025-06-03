from buddy import Buddy

# TODO: modify build to be OS-agnostic for dev/prod release split (testing on unix platforms)
#       SUB-TODO: create config-dev.py and add it to .gitignore.
#                 config.py will be on the main repo for OS-agnosticism, config-dev.py lives in dev for windows only

# TODO: add "transcription" mode where buddy just takes all the text it recognizes until it hears a key word then spits out the end result

# TODO: "save messages", "how many?", save w/e number is given

# TODO: Implement search.
#   When phrase "search" is detected in message, call ChatGPT API for real search function
if __name__ == "__main__":
    buddy = Buddy()
    buddy.run()