import os
import subprocess
import pyautogui
import time
import ctypes
import requests
from dotenv import load_dotenv

from ui.mascot import build_mascot
from ui.popup import show_popup
from utils.screenshot import capture_screen
from utils.config import config
from voice.listener import start_listening
from core.agent import process_command, classify_intent, get_conversation_response

load_dotenv()
ctypes.windll.shcore.SetProcessDpiAwareness(2)

def start_omniparser():
    process = subprocess.Popen(
        [config["omniparser"]["python_path"], config["omniparser"]["script"]],
        cwd=config["omniparser"]["dir"]
    )

    print("Starting OmniParser, please wait...")
    port = config["omniparser"]["port"]

    for _ in range(60):
        try:
            requests.get(f"http://127.0.0.1:{port}", timeout=1)
            print("OmniParser ready!")
            return process
        except:
            time.sleep(1)

    print("Warning: OmniParser may not be ready")
    return process

def on_command(root, text):
    # this is callback func passed to start_listening
    # for now print text to test
    print(f"Command received: {text}")

    if not text:
        return

    if "exit" in text and "program" in text:
        os._exit(0)

    intent = classify_intent(text)
    print(f"Intent: {intent}")

    if intent == "conversation":
        response = get_conversation_response(text)
        root.after(0, lambda: show_popup(root, response))
        return
    
    
    # # take a ss and print its size to confirm it works for now
    ss = capture_screen()
    result = process_command(text, ss)

    if not result:
        root.after(0, lambda: show_popup(root, "Could not process command. No result"))
        return

    if result.get("action") == "click":
        x = result.get("x")
        y = result.get("y")
        click_type = result.get("click_type", None)

        pyautogui.moveTo(x, y, duration=0.5)
        time.sleep(0.2)
        if click_type == "single":
            pyautogui.click()
        elif click_type == "double":
            pyautogui.doubleClick()
    elif result.get("action") == "not_found":
        root.after(0, lambda: show_popup(root, "Could not find target on screen."))
    # print(f"Screenshot captured: {ss.size}")

if __name__ == "__main__":
    omni_process = start_omniparser()
    root = build_mascot()
    start_listening(lambda text: on_command(root, text))
    root.mainloop()
    omni_process.terminate()

#Wake word must be call first for on_command