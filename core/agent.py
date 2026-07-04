import os
import io
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def process_command(command, screenshot):
    # convert PIL imgs to bytes
    img_bytes = io.BytesIO()
    screenshot.save(img_bytes, format="PNG")
    img_bytes = img_bytes.getvalue()

    # TODO: build a prompt that tells Gemini what to do
    prompt = f"""
    You are a desktop AI agent. The user said: '{command}'.
    Look at the screenshot and tell me:
    1. What is the user trying to do?
    2. What should I click or interact with?
    Reply in JSON like: {{"action": "click", "target": "chrome icon", "reasoning": "..."}}
    """

    # TODO: send prompt + screenshot to Gemini
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=[
            prompt, 
            types.Part.from_bytes(data=img_bytes, mime_type="image/png")
        ]
    )
    print(f"Gemini says: {response.text}")
