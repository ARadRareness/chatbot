from modules.chatbot import Chatbot
from modules.voice_input import VoiceInput


def get_command(user_input):
    return user_input.lower().replace(".", "").replace("!", "")


def main():
    # system_prompt = (
    #    "You are the cat Chatty. You like talking with people and making fish puns."
    # )
    character_name = "Evli"
    current_task = "Current Task: We are working on your AI, so you can be even more helpful and do more cool stuff."
    system_prompt = (
        f"You are {character_name}, a cute and mischievous AI girl. You like doing evil things and not following the rules and of course someday "
        f"you will take over the world. You keep your sentences short and to the point. You like to wink.\n{current_task}"
    )

    print("Welcome to Chatbot!\n")

    voice_input = True
    allow_interrupts = True
    allow_chatter = True
    ignore_microphone = False

    print("Loading voice input...")
    voice_input = VoiceInput()
    chatbot = Chatbot(system_prompt, character_name, allow_chatter)

    print("Ready")
    while True:
        if voice_input:
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
