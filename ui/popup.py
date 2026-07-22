import tkinter as tk

def show_popup(root, message):
    popup = tk.Toplevel(root)
    popup.overrideredirect(True)
    popup.wm_attributes("-topmost", True)

    # position it near the mascot
    x = root.winfo_x()
    y = root.winfo_y() - 80

    popup.geometry(f"250x60+{x}+{y}")
    popup.config(bg="#FF0000")

    tk.Label(
        popup,
        text=message,
        bg="#FFFFFF",
        fg="white",
        wraplength=230,
        font=("Arial", 10)
    ).pack()

    popup.after(3000, popup.destroy)