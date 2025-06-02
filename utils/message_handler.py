import os
import markdown
from datetime import datetime

class MessageHandler:
    def __init__(self):
        self.marked_messages = []

    def check_hey_buddy(self, text: str) -> bool:
        hey_buddy_keywords = [
            ['hey'],
            ['buddy']
        ]

        # check for phrase "hey buddy". list above can be altered for similar phrases, ie 'hello', 'hi'
        return all(any(k in text.lower() for k in keyword) for keyword in hey_buddy_keywords)
    
    def check_end_of_line(self, text: str) -> bool:
        end_of_line_keywords = [
            ['end'],
            ['of'],
            ['line']
        ]

        return all(any(k in text.lower() for k in keyword) for keyword in end_of_line_keywords)

    def mark_message(self, message: str):
        self.marked_messages.append(message)
    
    def check_mark_last_message(self, text: str) -> bool:
        mark_msg_keywords = ['mark', 'last', 'message']
        return all(word in text.lower() for word in mark_msg_keywords)
    
    def check_save_marked_messages(self, text: str) -> bool:
        save_content_keywords = [
            ['save'],
            ['mark', 'marked'],
            ['message', 'messages']
        ]

        # check if at least one entry in each list in save_content_keywords is in text
        return all(any(k in text.lower() for k in keyword) for keyword in save_content_keywords)

    # TODO: New implementation
    #   user says "save messages" and buddy asks how many?
    #   user gives a number, buddy saves last 5 of assistant+user messages
    def save_marked_messages(self, output_dir: str = "saved_messages"):
        if not self.marked_messages:
            print("No messages have been marked.")
            return False
        
        combined_message = "<br><br>".join(self.marked_messages)
        html_output = markdown.markdown(combined_message)
        os.makedirs(output_dir, exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_name = f"{timestamp}_saved_content.html"
        file_path = os.path.join(output_dir, file_name)

        with open(file_path, "w", encoding="utf-8") as f:
            f.write(self.convert_to_htmlcss(html_output))

    def convert_to_htmlcss(self, html_output: str) -> str:
        htmlcss_output = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/github-markdown-css/5.2.0/github-markdown.min.css">
                <style>
                    .markdown-body {{
                        box-sizing: border-box;
                        min-width: 200px;
                        max-width: 800px;
                        margin: 0 auto;
                        padding: 20px;
                    }}
                </style>
            </head>
            <body class="markdown-body">
                {html_output}
            </body>
            </html>
            """

        return htmlcss_output