import pyautogui
import numpy as np
import cv2
from PIL import Image

class WordleAutoPlayer:
    def __init__(self, screen_region, get_guess_fn, put_feedback_fn):
        """
        get_guess_fn: function () -> str
        put_feedback_fn: function (str) -> None
        """
        self.get_guess_fn = get_guess_fn
        self.put_feedback_fn = put_feedback_fn
        self.screen_region = screen_region

    def capture_board(self) -> Image.Image:
        """
        Captures and returns a screenshot of the defined Wordle screen region.
        """
        return pyautogui.screenshot(region=self.screen_region)

    def crop_to_tiles(self, image: Image.Image) -> Image.Image:
        """
        Detects all tile-like squares, finds the topmost row of 5 tiles,
        and tightly crops only that row with no extra padding.
        """
        img_np = np.array(image)
        edges = cv2.Canny(img_np, 30, 100)
        Image.fromarray(edges).show()

        
        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        tile_rects = []
        for cnt in contours:
            x, y, w, h = cv2.boundingRect(cnt)
            aspect = w / h
            bbox_area = w * h
            area = cv2.contourArea(cnt)
            solidity = area / bbox_area

            if 0.95 < aspect < 1.05 and 30 < w < 300 and solidity > 0.9:
                print(solidity)
                tile_rects.append((x, y, w, h))

        print(len(tile_rects))
        print(tile_rects)
        return image
        # if len(tile_rects) < 5:
        #     raise RuntimeError(f"Too few tiles found: {len(tile_rects)}")

        # # Sort by Y, then X
        # tile_rects.sort(key=lambda t: (t[1], t[0]))

        # # Group into rows by Y proximity
        # rows = []
        # current = []
        # last_y = None
        # for rect in tile_rects:
        #     x, y, w, h = rect
        #     if last_y is None or abs(y - last_y) <= 10:
        #         current.append(rect)
        #         last_y = y
        #     else:
        #         if len(current) == 5:
        #             rows.append(current)
        #         current = [rect]
        #         last_y = y
        # if len(current) == 5:
        #     rows.append(current)

        # if not rows:
        #     raise RuntimeError("No full row of 5 tiles found.")

        # # Get tight bounding box of topmost row
        # top_row = sorted(rows[0], key=lambda r: r[0])  # left-to-right
        # x_min = min(x for x, y, w, h in top_row)
        # y_min = min(y for x, y, w, h in top_row)
        # x_max = max(x + w for x, y, w, h in top_row)
        # y_max = max(y + h for x, y, w, h in top_row)

        # # Add no padding
        # cropped = img_np[y_min:y_max, x_min:x_max]
        # return Image.fromarray(cropped)

from select_region import select_screen_region

if __name__ == '__main__':
    region = select_screen_region()
    player = WordleAutoPlayer(region, None, None)
    board = player.capture_board()
    cropped = player.crop_to_tiles(board)
    cropped.show()
