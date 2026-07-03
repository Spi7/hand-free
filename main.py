import os

from ui.mascot import build_mascot
from voice.listener import start_listening

def on_command(text):
    # this is callback func passed to start_listening
    # for now print text to test
    print(f"Command received: {text}")

    if "exit" in text and "program" in text:
        os._exit(0)

if __name__ == "__main__":
    start_listening(on_command)
    build_mascot()

#Wake word must be call first for on_command