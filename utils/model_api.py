import requests

import json


class Model:
    def __init__(self, host_url, host_port):
        self.host_url = host_url
        self.host_port = host_port

    def generate_text(self, prompt, max_new_tokens=250):
        request = {
            "prompt": prompt,
            "max_new_tokens": max_new_tokens,
            "do_sample": True,
            "temperature": 0.7,
            "top_p": 0.1,
            "typical_p": 1,
            "repetition_penalty": 1.18,
            "top_k": 40,
            "min_length": 0,
            "no_repeat_ngram_size": 0,
            "num_beams": 1,
            "penalty_alpha": 0,
            "length_penalty": 1,
            "early_stopping": False,
            "seed": -1,
            "add_bos_token": True,
            "truncation_length": 2048,
            "ban_eos_token": False,
            "skip_special_tokens": True,
            "stopping_strings": [],
        }

        with open("_input.txt", "w", encoding="utf8") as file:
            file.write(prompt)

        url = f"http://{self.host_url}:{self.host_port}/api/v1/generate"

        response = requests.post(url, json=request)

        with open("_output.json", "w") as file:
            json.dump(response.json(), file)

        if response.status_code == 200:
            return response.json()["results"][0]["text"].strip()

        return ""
