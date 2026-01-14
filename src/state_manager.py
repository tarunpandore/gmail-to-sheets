import os

STATE_FILE = "processed_ids.txt"

def load_processed_ids():
    if not os.path.exists(STATE_FILE):
        return set()

    with open(STATE_FILE, "r") as f:
        return set(line.strip() for line in f.readlines())


def save_processed_id(message_id):
    with open(STATE_FILE, "a") as f:
        f.write(message_id + "\n")