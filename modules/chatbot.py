import re
import time
import threading
import queue

from utils.model_api import Model
from modules.chatter import Chatter
from modules.memory import Memory
from modules.prompt_manager import PhindFormat
from modules.voice_output import VoiceOutput


def filter_non_verbal_text(message):
    message = message.replace("*wink*", " wink! ")
    message = message.replace("*heart*", " heart!")
    # Remove text enclosed in "**"
    message = re.sub(r"\*[^*]*\*", "", message)

    # Remove emojis
    message = re.sub(r"[^\x00-\x7F]+", "", message)

    return message


def initialize_memory(character_folder_path):
    folder_path = "memories"
    number_of_retrieved_documents = 1

    return Memory(folder_path, character_folder_path, number_of_retrieved_documents)


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


class ChatbotThread(threading.Thread):
    def __init__(self, message_queue, character, allow_chatter=False):
        threading.Thread.__init__(self)

        self.message_queue = message_queue
        self.character = character

        self.chatter = None

        self.chatter = Chatter(allow_chatter, character.character_name)

        self.chat_handler = ChatHandler()

        self.load_chatbot()

        self.daemon = True
        self.start()

    def load_chatbot(self):
        self.model = Model("192.168.1.101", "5000")

        print("Loading memory...")
        self.memory = initialize_memory(self.character.folder_path)

        print("Loading voice output...")
        self.voice_output = VoiceOutput(self.character.voice_name)

    def run(self):
        t_running = True

        while t_running:
            if self.message_queue.empty():
                time.sleep(0.1)
                if self.voice_output.is_playing():
                    self.chatter.reset_timer()
                elif self.chatter.is_time_to_talk():
                    chatter_theme = self.chatter.get_chatter_theme()

                    response = self.respond_to_chatter(chatter_theme)
                    self.chatter.reset_timer()

                    if response:
                        self.memory.append_message("ASSISTANT", response)

            else:
                command, message = self.message_queue.get()
                if command == "exit":
                    t_running = False
                elif command == "input":
                    self.chatter.reset_timer()
                    self.respond_to_input(message)
                elif command == "interrupt":
                    self.voice_output.interrupt()

    def respond_to_chatter(self, chatter_theme):
        response = self.chat_handler.handle_chatter(
            self.character.system_prompt,
            self.character.character_name,
            chatter_theme,
            self.model,
            self.memory,
            self.voice_output,
        )

        if response:
            self.memory.append_message("ASSISTANT", response)

    def respond_to_input(self, user_input):
        self.memory.append_message("USER", user_input)

        response = self.chat_handler.handle_response(
            self.character.system_prompt,
            self.character.character_name,
            self.model,
            self.memory,
            self.voice_output,
        )

        if response:
            self.memory.append_message("ASSISTANT", response)


class Chatbot:
    def __init__(self, character, allow_chatter=False):
        self.message_queue = queue.Queue()

        self.chatbot_thread = ChatbotThread(
            self.message_queue, character, allow_chatter
        )

    def __del__(self):
        self.message_queue.put(("exit", ""))
        self.chatbot_thread.join()

    def input(self, message):
        self.message_queue.put(("input", message))

    def interrupt(self):
        self.message_queue.put(("interrupt", ""))
