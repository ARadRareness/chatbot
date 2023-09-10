from langchain.document_loaders import DirectoryLoader
from langchain.embeddings import HuggingFaceInstructEmbeddings
from langchain.vectorstores import FAISS
from langchain.document_loaders import TextLoader

from collections import namedtuple

import os


def load_documents(folder_path):
    return DirectoryLoader(folder_path, loader_cls=TextLoader).load()


def load_vector_store(documents):
    instructor_embeddings = HuggingFaceInstructEmbeddings(
        model_name="BAAI/bge-large-en", model_kwargs={"device": "cuda"}
    )

    return FAISS.from_documents(documents, instructor_embeddings)


class Memory:
    def __init__(self, folder_path, num_of_retrieved_documents=1):
        self.folder_path = folder_path
        self.num_of_retrieved_documents = num_of_retrieved_documents

        if num_of_retrieved_documents > 0:
            self.documents = load_documents(folder_path)
            self.vector_store = load_vector_store(self.documents)
            self.retriever = self.vector_store.as_retriever(
                search_kwargs={"k": num_of_retrieved_documents}
            )

        self.chat_history_filename = "previous_conversation.txt"
        self.chat_history = []
        self.load_history()

    def get_relevant_documents(self, message):
        if self.num_of_retrieved_documents > 0:
            retrieved_documents = self.retriever.get_relevant_documents(message)
            return retrieved_documents
        else:
            Document = namedtuple("Document", ["page_content"])
            return [Document("")]

    def append_message(self, role, message):
        self.chat_history.append((role, message))
        self.append_save_history(role, message)

    def append_save_history(self, role, message):
        with open(self.chat_history_filename, "a", encoding="utf8") as file:
            file.write(f"{role}\t{message}\n")

    def save_history(self):
        with open(self.chat_history_filename, "w", encoding="utf8") as file:
            for message in self.chat_history:
                file.write(f"{message[0]}\t{message[1]}\n")

    def load_history(self):
        if not os.path.exists(self.chat_history_filename):
            return

        with open(self.chat_history_filename, "r", encoding="utf8") as file:
            self.chat_history = []
            for line in file:
                line = line.strip().split("\t")
                if len(line) == 2:
                    self.chat_history.append(line)

    def get_message_history(self, number_of_messages, fix_repeaters=False):
        history = self.chat_history[-number_of_messages::]

        if fix_repeaters and len(history) >= 3:
            bot_replies = [
                msg[1] for msg in reversed(history) if msg[0] == "ASSISTANT"
            ][:3]

            if len(bot_replies) == 3:
                prefix = ""
                for i in range(min(map(len, bot_replies))):
                    if all(msg[i] == bot_replies[0][i] for msg in bot_replies):
                        prefix += bot_replies[0][i]
                    else:
                        break

                history = [
                    (msg[0], msg[1][len(prefix) :])
                    if msg[1].startswith(prefix)
                    else msg
                    for msg in history
                ]

        return history
