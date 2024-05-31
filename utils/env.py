# utils/env.py
import json
import os

CONFIG_FILE = 'config.json'

def set_env_variable(key, value):
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r') as file:
            config = json.load(file)
    else:
        config = {}

    config[key] = value

    with open(CONFIG_FILE, 'w') as file:
        json.dump(config, file)

def get_env_variable(key):
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r') as file:
            config = json.load(file)
        return config.get(key)
    return None
