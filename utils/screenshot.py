import mss
from PIL import Image

def capture_screen():
    with mss.mss() as screen:
        # TODO: capture full screenn
        raw_img = screen.grab(screen.monitors[0])

        # TODO: convert raw mss data to a PIL Image
        img = Image.frombytes("RGB", (raw_img.width, raw_img.height), raw_img.rgb)
        return img