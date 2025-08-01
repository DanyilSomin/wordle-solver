import time
import pyautogui
import cv2
import tkinter as tk
import numpy as np
from PIL import Image

def crop_region_to_tiles(region):
    """
    Detects all tile-like squares, finds the topmost row of 5 tiles,
    and tightly crops only that row with no extra padding.
    """
    image = pyautogui.screenshot(region = region)
    
    img_np = np.array(image)
    edges = cv2.Canny(img_np, 30, 100)
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    tile_rects = []
    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)
        aspect = w / h
        bbox_area = w * h
        area = cv2.contourArea(cnt)
        solidity = area / bbox_area
    
        if 0.95 < aspect < 1.05 and 30 < w < 300 and solidity == 0:
            tile_rects.append((x, y, w, h))

    assert(len(tile_rects) == 30 and 'Failed to find empty Wordle board on a screen.')

    x_min = min(x for x, y, w, h in tile_rects) + region[0]
    y_min = min(y for x, y, w, h in tile_rects) + region[1]
    x_max = max(x + w for x, y, w, h in tile_rects) + region[0]
    y_max = max(y + h for x, y, w, h in tile_rects) + region[1]

    return (x_min, y_min, x_max - x_min, y_max - y_min)

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


def extract_tile_colors(region) -> list[str]:
    """
    Takes a cropped screenshot of the full 6x5 Wordle board.
    Returns a list of 6 strings with tile color codes:
    'G' = green, 'Y' = yellow, 'B' = gray, '' = empty (unguessed).
    """
    image = pyautogui.screenshot(region=region)
    img_np = np.array(image)
    height, width, _ = img_np.shape
    tile_h = height // 6
    tile_w = width // 5

    color_codes = []

    for row in range(6):
        row_code = ''
        for col in range(5):
            y1 = row * tile_h
            y2 = (row + 1) * tile_h
            x1 = col * tile_w
            x2 = (col + 1) * tile_w

            tile = img_np[y1:y2, x1:x2]

            avg_color = tile.mean(axis=(0, 1))
            r, g, b = avg_color

            max_rgb = max(r, g, b)
            min_rgb = min(r, g, b)
            r = r - min_rgb
            g = g - min_rgb
            b = b - min_rgb

            # Color classification
            if g > 10 and r < 10 and b < 10:
                row_code += 'G'  # Green
            elif r > 10 and g > 10 and b < 10:
                row_code += 'Y'  # Yellow
            elif r < 10 and g < 10 and b < 10 and max_rgb > 50:
                row_code += 'B'  # Gray
            elif r < 10 and g < 10 and b < 10 and max_rgb < 30:
                row_code += ''   # Empty or unknown
            else: 
                print(f"Row: {row}. Col: {col}.")
                print(f"R: {r}, G: {g}, B: {b}.")
                assert(False and "Error matching letter colors")

        color_codes.append(row_code)

    return color_codes


def type_word_at_center(region: tuple[int, int, int, int], word: str, delay: float = 0.1):
    """
    Focuses the center of the region and types the given word followed by ENTER.

    Parameters:
        region: (left, top, width, height) of the Wordle game area.
        word: The 5-letter word to type.
        delay: Optional delay between actions in seconds (default 0.1s).
    """
    left, top, width, height = region
    center_x = left + width // 2
    center_y = top + height // 2

    # Move mouse and click to focus
    pyautogui.click(center_x, center_y)
    time.sleep(delay)

    # Type the word and press Enter
    pyautogui.typewrite(word, interval=delay)
    pyautogui.press('enter')
