from buddy import Buddy

# TODO: get build OS-agnostic for dev/prod release split

# TODO: add "transcription" mode where buddy just takes all the text it recognizes until it hears a key word then spits out the end result

# TODO: "save messages", "how many?", save w/e number is given

# TODO: Find a way to use new voices (I installed the natural Jenny voice, try it out)
#   https://github.com/gexgd0419/NaturalVoiceSAPIAdapter can use this for Jenny voice, check if it's good first

# TODO: Implement search.
#   When phrase "search" is detected in message, call ChatGPT API for real search function
if __name__ == "__main__":
    buddy = Buddy()
    buddy.run()