import tkinter as tk

def show_popup(root, message):
    popup = tk.Toplevel(root)
    popup.overrideredirect(True)
    popup.wm_attributes("-topmost", True)

    # position the popup above the mascot
    x = root.winfo_x() - 30
    y = root.winfo_y() - 90
    popup.geometry(f"280x70+{x}+{y}")

    # cyberpunk color scheme
    BG_COLOR = "#1a1a2e"       # dark navy background
    BORDER_COLOR = "#e94560"   # red border
    TEXT_COLOR = "#00ff99"     # neon green text
    FONT = ("Courier", 10, "bold")  # monospace for pixel feel

    # red border frame wrapping the whole popup
    border_frame = tk.Frame(popup, bg=BORDER_COLOR, padx=2, pady=2)
    border_frame.pack(fill="both", expand=True)

    # dark inner frame inside the border
    inner_frame = tk.Frame(border_frame, bg=BG_COLOR, padx=8, pady=6)
    inner_frame.pack(fill="both", expand=True)

    # small arrow accent in top left corner
    tk.Label(inner_frame, text="▶", bg=BG_COLOR, fg=BORDER_COLOR, font=FONT).place(x=0, y=0)

    # text label — starts empty, typewriter fills it in
    label = tk.Label(
        inner_frame,
        text="",
        bg=BG_COLOR,
        fg=TEXT_COLOR,
        font=FONT,
        wraplength=240,
        anchor="w",
        justify="left"
    )
    label.pack(fill="both", expand=True, padx=15)

    # typewriter effect — reveals message one character at a time
    def typewrite(i=0):
        if i <= len(message):
            # show typed text so far + blinking cursor block
            cursor = "█" if i < len(message) else ""
            label.config(text=message[:i] + cursor)
            popup.after(40, lambda: typewrite(i + 1))

    typewrite()

    # fade out — gradually reduces opacity before destroying
    def fade_out(alpha=1.0):
        if alpha > 0:
            try:
                popup.attributes("-alpha", alpha)
                popup.after(50, lambda: fade_out(round(alpha - 0.05, 2)))
            except:
                pass
        else:
            try:
                popup.destroy()
            except:
                pass

    # start fading after 2.5 seconds
    popup.after(2500, fade_out)