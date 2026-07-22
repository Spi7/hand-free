import os
import tkinter as tk

from PIL import Image, ImageTk
from utils.drag import make_draggable

base_dir = os.path.dirname(os.path.abspath(__file__))
img_path = os.path.join(base_dir, "..", "assets", "ai agent pic 1.png")

def build_mascot():
    root = tk.Tk() # create the window obj

    root.bind("<Escape>", lambda e: os._exit(0)) # destroy process using esc -> e is an event object created
    #.geometry("WIDTHxHEIGHT+X+Y")
    width = 200
    height = 150

    x_pos = (root.winfo_screenwidth() - width)//2 #width
    y_pos = (root.winfo_screenheight() - height)//2 #height
    root.geometry(f"{width}x{height}+{x_pos}+{y_pos}") #the mascot start off in center

    # Since we're building a mascot, we would want to remove the title bar and back the background transparent
    # 1) .overrideredirect() -> controls titlebar | 2) .wm_attributes("-topmost", True)
    # Goal: keep always on top? make one color transparent

    root.overrideredirect(True) # remove title bar
    root.wm_attributes("-topmost", True) #this root window will be above all other windows
    root.wm_attributes("-transparentcolor", "#FFFFFF")
    root.config(bg="#FFFFFF")

    # Create a canvas for the mascot (placeholder?) -> later change to photo?
    canvas = tk.Canvas(
        root,
        width=width,
        height=height,
        bg="#FFFFFF",
        highlightthickness=0
    )
    # canvas.create_oval(20,20,180,90, fill="#8ACFFD") # placeholder for img

    image = Image.open(img_path)
    image = image.resize((width, height))
    photo = ImageTk.PhotoImage(image) #convert to tkinter-compatible format
    canvas.create_image(width//2, height//2, image=photo, anchor="center")
    canvas.image = photo

    canvas.pack() # place the canvas inside window and make it visible

    # Make the mascot draggable around the screen
    make_draggable(root=root, widget=canvas)
    root.bind("<FocusIn>", lambda e: root.geometry(f"{width}x{height}+{root.winfo_x()}+{root.winfo_y()}"))

    root.after(100, root.focus_force)
    return root # for popups use

    
    # -> Create words & Buttons for the window frame created
    # frame = tk.Frame(root)
    # frame.grid()
    # tk.Label(frame, text="hi").grid(column=0, row=0)
    # tk.Button(frame, text="Quit", command=root.destroy).grid(column=1, row=1)

# if __name__ == "__main__":
#     build_mascot()


#Learn about tk.Toplevel() later to create child window depend on root for popups