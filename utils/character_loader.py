import os
import yaml

CHARACTERS_FOLDER = "characters"
PROFILE_FILENAME = "character.yaml"


def load_character(folder_name):
    profile_path = os.path.join(CHARACTERS_FOLDER, folder_name, PROFILE_FILENAME)

    if os.path.exists(profile_path):
        try:
            with open(profile_path, "r", encoding="utf8") as file:
                profile = yaml.safe_load(file)
        except:
            print("Failed to load", profile_path)
            profile = {}
    else:
        profile = {}

    character_name = profile.get("character_name", "NO NAME")
    current_task = profile.get("current_task", "NO TASK").replace(
        "{character_name}", character_name
    )
    system_prompt = (
        profile.get("system_prompt", "NO SYSTEM PROMPT")
        .replace("{character_name}", character_name)
        .replace("{current_task}", current_task)
    )

    return Character(character_name, current_task, system_prompt)


class Character:
    def __init__(self, character_name, current_task, system_prompt):
        self.character_name = character_name
        self.current_task = current_task
        self.system_prompt = system_prompt
