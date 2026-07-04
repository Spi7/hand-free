import os

from ui.mascot import build_mascot
from utils.screenshot import capture_screen
from voice.listener import start_listening
from core.agent import process_command

def on_command(text):
    # this is callback func passed to start_listening
    # for now print text to test
    print(f"Command received: {text}")

    if "exit" in text and "program" in text:
        os._exit(0)
    
    # # take a ss and print its size to confirm it works for now
    ss = capture_screen()
    process_command(text, ss)
    # print(f"Screenshot captured: {ss.size}")

if __name__ == "__main__":
    start_listening(on_command)
    build_mascot()

#Wake word must be call first for on_command