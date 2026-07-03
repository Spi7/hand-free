# "<ButtonPress-1>"    → left mouse button pressed down
# "<ButtonRelease-1>"  → left mouse button released
# "<B1-Motion>"        → mouse moving while left button held
# "<ButtonPress-3>"    → right mouse button pressed
# "<Double-Button-1>"  → left mouse button double clicked
# "<Enter>"            → mouse enters the widget
# "<Leave>"            → mouse leaves the widget

def make_draggable(root, widget):
    # root -> tk.Tk() | widget -> canvas (what user clicks and drags on)
    root.start_x = None
    root.start_y = None

    def on_drag(event):
        # TODO: store the starting MOUSE position
        root.start_x = event.x 
        root.start_y = event.y
    
    def on_motion(event):
        # TODO: calculate new window position and move it
        pos_x = root.winfo_x() + event.x - root.start_x # event.x is current moving mouse pos
        pos_y = root.winfo_y() + event.y - root.start_y
        root.geometry(f"+{pos_x}+{pos_y}")
    
    
    widget.bind("<ButtonPress-1>", on_drag)
    widget.bind("<B1-Motion>", on_motion)
    # widget.bind("<ButtonPress-1>", lambda e: on_drag(e))
    # widget.bind("<B1-Motion>", lambda e: on_motion(e))
    # widget.bind("<ButtonRelease-1>", lambda e: end_drag(e))