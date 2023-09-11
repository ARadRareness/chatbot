from modules.chatbot import Chatbot
from modules.voice_input import VoiceInput
from utils.character_loader import load_character


def get_command(user_input):
    return user_input.lower().replace(".", "").replace("!", "")


def main():
    character_to_load = input("Which character do you want to load? ")
    character = load_character(character_to_load)

    print("CHARACTER PROFILE:", character.system_prompt)

    print("\nWelcome to Chatbot!\n")

    use_voice_input = True
    allow_interrupts = True
    allow_chatter = True
    ignore_microphone = False

    print("Loading voice input...")
    voice_input = VoiceInput()
    chatbot = Chatbot(character, allow_chatter)

    print("Ready")
    while True:
        if use_voice_input:
            user_input = voice_input.get_input()
            print("Chat:", user_input)
        else:
            user_input = input("Chat: ")

        if allow_interrupts:
            chatbot.interrupt()

        if not user_input or get_command(user_input) == "exit program":
            break

        if (
            get_command(user_input) == "stop microphone"
            or get_command(user_input) == "microphone off"
        ):
            ignore_microphone = True
            print("Microphone OFF")
        elif (
            get_command(user_input) == "start microphone"
            or get_command(user_input) == "microphone on"
        ):
            ignore_microphone = False
            print("Microphone ON")

        if not ignore_microphone:
            chatbot.input(user_input)


if __name__ == "__main__":
    main()
