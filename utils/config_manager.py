import json
import os

CONFIG_PATH = "config.json"

DEFAULT_CONFIG = {
    "download_path": os.path.expanduser("~/Downloads"),
    "theme": "dark",
    "version": "1.0.0"
}


class ConfigManager:

    def __init__(self):
        if not os.path.exists(CONFIG_PATH):
            self.save(DEFAULT_CONFIG)

        self.config = self.load()

    def load(self):
        with open(CONFIG_PATH, "r") as f:
            return json.load(f)

    def save(self, data):
        with open(CONFIG_PATH, "w") as f:
            json.dump(data, f, indent=4)

    def get(self, key):
        return self.config.get(key)

    def set(self, key, value):
        self.config[key] = value
        self.save(self.config)