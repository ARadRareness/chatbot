import random
import time


class Chatter:
    def __init__(self, is_enabled, character_name):
        self.is_enabled = is_enabled
        self.character_name = character_name

        self.reset_timer()

    def is_time_to_talk(self):
        if not self.is_enabled:
            return False

        current_time = time.time()

        if not self.next_chatter_time:
            self.next_chatter_time = current_time + random.randint(20, 60)

        if current_time >= self.next_chatter_time:
            return True

        return False

    def reset_timer(self):
        self.next_chatter_time = None

    def get_chatter_theme(self):
        theme = random.choice(
            [
                self.create_statement,
                self.ask_question,
                self.tell_joke,
                self.tell_story,
                self.filler_words,
                self.try_to_change_topic,
                self.brainstorm,
            ]
        )

        return theme()

    def create_statement(self):
        return random.choice(
            [
                "a statement about something that "
                + self.character_name
                + " is passionate about",
                "a summarization of the current conversation followed by a question",
            ]
        )

    def ask_question(self):
        return random.choice(
            [
                "a question that "
                + self.character_name
                + " is curious to find out about the user or the current conversation",
                "a philosopical question that you and the user will both be interested in discussing",
            ]
        )

    def tell_joke(self):
        return random.choice(
            [
                "a joke that you personally find hilarious",
                "a joke that you really love",
                "a joke that the user will like",
                "a joke about something you are passionate about",
            ]
        )

    def tell_story(self):
        return random.choice(
            [
                "a story from " + self.character_name + "'s personal life",
                "a story about something you have heard",
                "a story related to the current topic",
            ]
        )

    def try_to_change_topic(self):
        return random.choice(
            [
                "about trying to change the current topic",
                "about changing the topic to something that the user will really enjoy talking about",
                "about changing the topic to something that "
                + self.character_name
                + " will really enjoy talking about",
            ]
        )

    def filler_words(self):
        return "a word such as, wink, heart, hmm, or mmm to show interest"

    def brainstorm(self):
        return "an idea for improvements concerning the current topic"
