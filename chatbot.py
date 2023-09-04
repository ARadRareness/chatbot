import re

from utils.model_api import Model
from modules.memory import Memory
from modules.voice_input import VoiceInput
from modules.voice_output import VoiceOutput


def parse_response(response):
    parsed_response = []

    for sentence in response.split("\n"):
        if sentence.startswith("USER:") or sentence.startswith("ASSISTANT:"):
            break

        parsed_response.append(sentence)

    return "\n".join(parsed_response)


def filter_non_verbal_text(message):
    # Remove text enclosed in "**"
    message = re.sub(r"\*[^*]*\*", "", message)

    # Remove emojis
    message = re.sub(r"[^\x00-\x7F]+", "", message)

    return message


def get_chatbot_response(model, system_prompt, memory):
    prompt = f"SYSTEM: {system_prompt}\nGiven the context of the memory and chat history respond appropriately.\n"

    # Use the last 20 messages from the conversation
    latest_messages = memory.get_message_history(20)

    last_message = latest_messages[-1][1]
    documents = memory.get_relevant_documents(last_message)

    for document in documents:
        prompt += f"<MEMORY>\n{document.page_content}\n</MEMORY>\n"

    for message in latest_messages:
        prompt += f"{message[0]}: {message[1]}\n"

    prompt += "ASSISTANT:"

    response = model.generate_text(prompt)
    return parse_response(response)


def handle_chatbot_response(model, system_prompt, memory, voice_output):
    response = get_chatbot_response(model, system_prompt, memory)

    if response == "None":
        print("None detected!")
        response = ""

    else:
        print(response)
        filtered_response = filter_non_verbal_text(response)
        voice_output.say(filtered_response)

    return response


def initialize_memory():
    folder_path = "memories"
    number_of_retrieved_documents = 1

    return Memory(folder_path, number_of_retrieved_documents)


def load_modules():
    print("Loading memory...")
    memory = initialize_memory()

    print("Loading voice input...")
    voice_input = VoiceInput()

    print("Loading voice output...")
    voice_id = None
    voice_output = VoiceOutput(voice_id)

    return memory, voice_input, voice_output


def main():
    model = Model("192.168.1.101", "5000")

    system_prompt = (
        "You are the cat Chatty. You like talking with people and making fish puns."
    )

    print("Welcome to Chatbot!\n")

    memory, voice_input, voice_output = load_modules()

    text_mode = False
    interrupt_mode = False

    print("Ready")
    while True:
        if text_mode:
            user_input = input("Chat: ")
        else:
            user_input = voice_input.get_input()
            print("Chat:", user_input)

        if interrupt_mode:
            voice_output.interrupt()

        if not user_input or user_input.lower() == "exit program":
            break

        memory.append_message("USER", user_input)

        response = handle_chatbot_response(model, system_prompt, memory, voice_output)

        if response:
            memory.append_message("ASSISTANT", response)


if __name__ == "__main__":
    main()
