class PromptFormat:
    def __init__(self):
        self.response_format = """
    SYSTEM: <<SYSTEM_PROMPT>>
    Given the context of the memory and chat history respond appropriately.
    <<MEMORY>>
    <<CHAT_HISTORY>>
    ASSISTANT:
"""
        self.chatter_format = """
    SYSTEM: <<SYSTEM_PROMPT>>
    Given the context of the memory and chat history respond appropriately. The reply should be <<CHATTER_THEME>>.
    <<MEMORY>>
    <<CHAT_HISTORY>>
    ASSISTANT:
"""

    def get_response(self, system_prompt, character_name, memory):
        # Use the last 20 messages from the conversation
        latest_messages = memory.get_message_history(20, fix_repeaters=True)

        if len(latest_messages) > 0:
            last_message = latest_messages[-1][1]
        else:
            last_message = ""

        documents = memory.get_relevant_documents(last_message)

        memory_message = ""
        for document in documents:
            memory_message += f"<MEMORY>\n{document.page_content}\n</MEMORY>\n"

        chat_history = ""
        for message in latest_messages:
            chat_history += f"{message[0]}: {message[1]}\n"

        return (
            self.response_format.replace("<<SYSTEM_PROMPT>>", system_prompt)
            .replace("<<MEMORY>>", memory_message)
            .replace("<<CHAT_HISTORY>>", chat_history)
            .replace("<<CHARACTER>>", character_name)
        )

    def get_chatter(self, system_prompt, chatter_theme, character_name, memory):
        # Use the last 20 messages from the conversation
        latest_messages = memory.get_message_history(20, fix_repeaters=True)

        if len(latest_messages) > 0:
            last_message = latest_messages[-1][1]
        else:
            last_message = ""

        documents = memory.get_relevant_documents(last_message)

        memory_message = ""
        for document in documents:
            memory_message += f"<MEMORY>\n{document.page_content}\n</MEMORY>\n"

        chat_history = ""
        for message in latest_messages:
            chat_history += f"{message[0]}: {message[1]}\n"

        return (
            self.chatter_format.replace("<<SYSTEM_PROMPT>>", system_prompt)
            .replace("<<MEMORY>>", memory_message)
            .replace("<<CHAT_HISTORY>>", chat_history)
            .replace("<<CHARACTER>>", character_name)
            .replace("<<CHATTER_THEME>>", chatter_theme)
        )


class PhindFormat(PromptFormat):
    def __init__(self):
        PromptFormat.__init__(self)
        self.response_format = """
### System Prompt
<<SYSTEM_PROMPT>>

### User Message
<<MEMORY>>
<<CHAT_HISTORY>>
Given the context of your memory and chat history, write <<CHARACTER>>'s next chat reply. Write a single reply only. Stay in character at all times.
When the user asks a question, answer it.
### Assistant
<<CHARACTER>>:
"""
        self.chatter_format = """
### System Prompt
<<SYSTEM_PROMPT>>

### User Message
<<MEMORY>>
<<CHAT_HISTORY>>
Given the context of your memory and chat history, write <<CHARACTER>>'s next chat reply. Write a single reply only. Stay in character at all times.
The reply should be <<CHATTER_THEME>>.
### Assistant
<<CHARACTER>>:
"""
