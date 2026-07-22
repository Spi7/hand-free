import os
import io
import json
import re
import ast
import tempfile
from google import genai
from google.genai import types
from gradio_client import Client, handle_file
from utils.config import config

gemini_client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
omni_client = None

def get_omni_client():
    global omni_client
    if omni_client is None:
        omni_client = Client(f"http://127.0.0.1:{config['omniparser']['port']}")
    return omni_client

def parse_screen(screenshot):
    # save ss to tmp file for gradio_client
    with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmp:
        tmp_path = tmp.name
        screenshot.save(tmp_path)
    
    try:
        client = get_omni_client()
        result = omni_client.predict(
            image_input = handle_file(tmp_path),
            box_threshold = 0.05,
            iou_threshold = 0.1,
            use_paddleocr = False,
            imgsz = 640,
            api_name = "/process"
        )

        # result is a tuple: (image_path, elements_strings)
        elements_string = result[1]
        return elements_string
    except Exception as e:
        print(f"OmniParser error screen: {e}")
        return
    finally:
        os.remove(tmp_path)


def parse_elements(element_str):
    if not element_str:
        return []
    elements = []
    for line in element_str.strip().split('\n'):
        match = re.match(r'icon \d+: (.+)', line)
        if match:
            try:
                element = ast.literal_eval(match.group(1))
                elements.append(element)
            except Exception as e:
                print(f"Failed to parse element: {e}")
                continue
    return elements

def process_command(command, screenshot):

    width = screenshot.width
    height = screenshot.height

    # get all elemetns from OmniParser
    element_str = parse_screen(screenshot)
    elements = parse_elements(element_str)

    # keep prompt minimized
    simplified = []
    for i, element in enumerate(elements):
        simplified.append({"index": i, "content": element.get("content", "")})
    
    # TODO: send prompt + screenshot to Gemini
    match_prompt = f"""
    The user said: '{command}'. Look at the SCREENSHOT to visually identify UI elements.
    Here are the detected UI elements with their positions: {json.dumps(simplified)}
    Ignore any text found inside terminals, code editors, or chat windows. Only match actual clickable UI elements like icons, buttons, taskbar items, desktop shortcuts.
    Some icons have generic labels like '3D cube' or folder -- use the screenshot to identify what they actually are.
    Also determine click_type:
    - "double" if opening an app or file from the desktop or file explorer
    - "single" for taskbar icons, buttons, links, or in-game UI elements
    Reply ONLY in JSON:
    {{"index": 0, "click_type": "single", "reasoning": "..."}}
    If nothing matches: {{"index": -1, "reasoning": "..."}}
    """
    img_bytes = io.BytesIO()
    screenshot.save(img_bytes, format="PNG")
    img_bytes = img_bytes.getvalue()
    
    match_response = gemini_client.models.generate_content(
        model=config["gemini"]["model"],
        contents=[match_prompt, types.Part.from_bytes(data=img_bytes, mime_type="image/png")]
    )

    match_text = re.sub(r'```json|```', '', match_response.text).strip()
    match = json.loads(match_text)

    index = match.get("index")
    print(f"Gemini picked index: {index}")

    if index == -1 or index is None:
        return {"action": "not_found", "reasoning": match.get("reasoning")}

    if index >= len(elements) or index < 0:
        print(f"Invalid index {index}, only {len(elements)} elements detected")
        return {"action": "not_found", "reasoning": "Invalid element index returned"}

    # Convert normalized bbox to pixel coord
    element = elements[index]
    box = element["bbox"]  # [x_min, y_min, x_max, y_max] normalized 0-1

    xmin = int(box[0] * width)
    ymin = int(box[1] * height)
    xmax = int(box[2] * width)
    ymax = int(box[3] * height)

    # center of the bounding box
    x = (xmin + xmax) // 2
    y = (ymin + ymax) // 2

    print(f"Found: {element['content']} at ({x}, {y})")
    print(f"Found: {element.get('content', 'unknown')} at ({x}, {y})")

    return {"action": "click", "x": x, "y": y, "click_type": match.get("click_type", None), "reasoning": match.get("reasoning")}