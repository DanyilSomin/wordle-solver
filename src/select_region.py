import tkinter as tk

def select_screen_region():
    """
    Opens a transparent fullscreen window to let user draw a rectangle.
    Returns (left, top, width, height)
    """
    region = {}
    rect_id = None

    def on_mouse_down(event):
        region['x1'] = event.x_root
        region['y1'] = event.y_root
        region['x2'] = event.x_root
        region['y2'] = event.y_root
        nonlocal rect_id
        rect_id = canvas.create_rectangle(event.x, event.y, event.x, event.y, outline='red', width=2)

    def on_mouse_move(event):
        if rect_id is not None:
            canvas.coords(rect_id, region['x1'] - root.winfo_rootx(), region['y1'] - root.winfo_rooty(),
                                      event.x_root - root.winfo_rootx(), event.y_root - root.winfo_rooty())

    def on_mouse_up(event):
        region['x2'] = event.x_root
        region['y2'] = event.y_root
        root.quit()

    root = tk.Tk()
    root.attributes("-alpha", 0.3)
    root.attributes("-fullscreen", True)
    root.attributes("-topmost", True)
    root.configure(bg='black')

    canvas = tk.Canvas(root, bg='black', highlightthickness=0)
    canvas.pack(fill=tk.BOTH, expand=True)

    root.bind("<ButtonPress-1>", on_mouse_down)
    root.bind("<B1-Motion>", on_mouse_move)
    root.bind("<ButtonRelease-1>", on_mouse_up)

    root.mainloop()
    root.destroy()

    x1, y1 = region['x1'], region['y1']
    x2, y2 = region['x2'], region['y2']
    left = min(x1, x2)
    top = min(y1, y2)
    width = abs(x2 - x1)
    height = abs(y2 - y1)

    return (left, top, width, height)

if __name__ == '__main__':
    print(select_screen_region())
