import datetime


class PromptFormat:
    def __init__(self):
        self.response_format = """
    SYSTEM: <<SYSTEM_PROMPT>>
    Given the context of the memory and chat history respond appropriately.
    <<MEMORY>>
    <<CHAT_HISTORY>>
    Today is <<DAYOFWEEK>>, the clock is <<HOURANDMINUTES>> and the date is <<DATE>>.
    ASSISTANT:"""
        self.chatter_format = """
    SYSTEM: <<SYSTEM_PROMPT>>
    Given the context of the memory and chat history respond appropriately. The reply should be <<CHATTER_THEME>>.
    <<MEMORY>>
    <<CHAT_HISTORY>>
    Today is <<DAYOFWEEK>>, the clock is <<HOURANDMINUTES>> and the date is <<DATE>>.
    ASSISTANT:"""

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

        now = datetime.datetime.now()

        return (
            self.response_format.replace("<<SYSTEM_PROMPT>>", system_prompt)
            .replace("<<MEMORY>>", memory_message)
            .replace("<<CHAT_HISTORY>>", chat_history)
            .replace("<<CHARACTER>>", character_name)
            .replace("<<DAYOFWEEK>>", now.strftime("%A"))
            .replace("<<HOURANDMINUTES>>", now.strftime("%H:%M"))
            .replace("<<HOUR>>", now.strftime("%H"))
            .replace("<<MINUTE>>", now.strftime("%M"))
            .replace("<<DATE>>", now.strftime("%Y-%m-%d"))
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

        now = datetime.datetime.now()

        return (
            self.chatter_format.replace("<<SYSTEM_PROMPT>>", system_prompt)
            .replace("<<MEMORY>>", memory_message)
            .replace("<<CHAT_HISTORY>>", chat_history)
            .replace("<<CHARACTER>>", character_name)
            .replace("<<CHATTER_THEME>>", chatter_theme)
            .replace("<<DAYOFWEEK>>", now.strftime("%A"))
            .replace("<<HOURANDMINUTES>>", now.strftime("%H:%M"))
            .replace("<<HOUR>>", now.strftime("%H"))
            .replace("<<MINUTE>>", now.strftime("%M"))
            .replace("<<DATE>>", now.strftime("%Y-%m-%d"))
        )


class PhindFormat(PromptFormat):
    def __init__(self):
        PromptFormat.__init__(self)

        self.response_format = """
### System Prompt
<<SYSTEM_PROMPT>>

### User Message
<<MEMORY>>
<MEMORY>
You know that it is <<DAYOFWEEK>> today.
Today is <<DAYOFWEEK>>.
The current day is <<DAYOFWEEK>>.
When asked what the current day is, answer with <<DAYOFWEEK>>.
You know that the clock is <<HOURANDMINUTES>>.
The clock is <<HOURANDMINUTES>>.
The time is <<HOURANDMINUTES>>.
The current hour is <<HOUR>> and the minute is <<MINUTE>>.
The current date is <<DATE>>.
</MEMORY>

<<CHAT_HISTORY>>
Given the context of your memory and chat history, write <<CHARACTER>>'s next chat reply. Write a single reply only. Stay in character at all times.
When the user asks a question, answer it. Take a deep breath and answer to the best of your ability.
### Assistant
<<CHARACTER>>:"""

        self.chatter_format = """
### System Prompt
<<SYSTEM_PROMPT>>

### User Message
<<MEMORY>>
<MEMORY>
You know that it is <<DAYOFWEEK>> today.
Today is <<DAYOFWEEK>>.
The current day is <<DAYOFWEEK>>.
When asked what the current day is, answer with <<DAYOFWEEK>>.
You know that the clock is <<HOURANDMINUTES>>.
The clock is <<HOURANDMINUTES>>.
The time is <<HOURANDMINUTES>>.
The current hour is <<HOUR>> and the minute is <<MINUTE>>.
The current date is <<DATE>>.
</MEMORY>

<<CHAT_HISTORY>>
Given the context of your memory and chat history, write <<CHARACTER>>'s next chat reply. Write a single reply only. Stay in character at all times.
The reply should be <<CHATTER_THEME>>.
### Assistant
<<CHARACTER>>:"""
