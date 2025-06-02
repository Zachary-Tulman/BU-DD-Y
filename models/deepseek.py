from openai import OpenAI

class DeepSeekModel:
    def __init__(self, config):
        self.client = OpenAI(api_key=config.get("DEEPSEEK_API_KEY"), base_url="https://api.deepseek.com")
        self.messages = []

    def init_with_prompt(self, buddy_prompt):
        self.messages = [{
            "role": "system",
            "content": buddy_prompt
        }]

    def send_message(self, text: str) -> str:
        print("Thinking...")

        self.messages.append({
            "role": "user",
            "content": text
        })

        response = self.client.chat.completions.create(
            model="deepseek-chat",
            messages=self.messages,
            temperature=1.3,
            # TODO: find a way to speak_text as the response is streamed for less waiting
            #   ie stream=True
            stream=True,
        )
        
        return response
    
    def append_assistant_response(self, content):
        self.messages.append({
            "role": "assistant",
            "content": content
            })
    
    def get_last_response(self) -> str | None:
        if len(self.messages) >= 2 and self.messages[-1]["role"] == "assistant":
            return self.messages[-1]["content"]
        return None