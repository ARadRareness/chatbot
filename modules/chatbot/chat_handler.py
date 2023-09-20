import re

from modules.prompt_manager import PhindFormat


class ChatHandler:
    def __init__(self):
        self.prompt_formatter = self.prompt_formatter = PhindFormat()

    def parse_response(self, response):
        parsed_response = []

        for sentence in response.split("\n"):
            if sentence.startswith("USER:") or sentence.startswith("ASSISTANT:"):
                break

            parsed_response.append(sentence)

        return "\n".join(parsed_response)

    def get_chatbot_response(self, prompt, model, voice_output):
        generated_text = model.generate_text(prompt).replace("*winks*", "*wink*")
        response = self.parse_response(generated_text)

        print(response)
        filtered_response = filter_non_verbal_text(response)
        voice_output.say(filtered_response)

        return response

    def handle_chatter(
        self, system_prompt, character_name, chatter_theme, model, memory, voice_output
    ):
        prompt = self.prompt_formatter.get_chatter(
            system_prompt, chatter_theme, character_name, memory
        )

        return self.get_chatbot_response(prompt, model, voice_output)

    def handle_response(
        self, system_prompt, character_name, model, memory, voice_output
    ):
        prompt = self.prompt_formatter.get_response(
            system_prompt, character_name, memory
        )

        return self.get_chatbot_response(prompt, model, voice_output)


def filter_non_verbal_text(message):
    message = message.replace("*wink*", " wink! ")
    message = message.replace("*heart*", " heart!")
    # Remove text enclosed in "**"
    message = re.sub(r"\*[^*]*\*", "", message)

    # Remove emojis
    message = re.sub(r"[^\x00-\x7F]+", "", message)

    return message
