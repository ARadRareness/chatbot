import time
import threading
import queue

from modules.chatbot.chatter import Chatter
from modules.chatbot.chat_handler import ChatHandler
from modules.memory import Memory
from modules.voice_output import VoiceOutput
from utils.model_api import Model


def initialize_memory(character_folder_path):
    folder_path = "memories"
    number_of_retrieved_documents = 1

    return Memory(folder_path, character_folder_path, number_of_retrieved_documents)


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


class ChatbotThread(threading.Thread):
    def __init__(self, message_queue, character, allow_chatter=False):
        threading.Thread.__init__(self)

        self.message_queue = message_queue
        self.character = character

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
