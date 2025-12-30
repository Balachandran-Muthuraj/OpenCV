import numpy as np
import cv2
import time
import matplotlib.pyplot as plt
import os

class Sketcher:
    """OpenCV Utility class for mouse handling."""
    def __init__(self, windowname, dests, colors_func):
        self.prev_pt = None
        self.windowname = windowname
        self.dests = dests
        self.colors_func = colors_func
        self.dirty = False
        self.show()
        cv2.setMouseCallback(self.windowname, self.on_mouse)

    def show(self):
        cv2.imshow(self.windowname, self.dests[0])
        cv2.imshow(self.windowname + ": mask", self.dests[1])

    def on_mouse(self, event, x, y, flags, param):
        pt = (x, y)
        if event == cv2.EVENT_LBUTTONDOWN:
            self.prev_pt = pt
        elif event == cv2.EVENT_LBUTTONUP:
            self.prev_pt = None

        if self.prev_pt and flags & cv2.EVENT_FLAG_LBUTTON:
            for dst, color in zip(self.dests, self.colors_func()):
                cv2.line(dst, self.prev_pt, pt, color, 5)
            self.dirty = True
            self.prev_pt = pt
            self.show()

# 1. Setup Image Path
# Ensure you have an image in your project folder or provide an absolute path
filename = "images/515.jpg"

if not os.path.exists(filename):
    print(f"Error: {filename} not found. Please place an image in the 'images' folder.")
else:
    img = cv2.imread(filename, cv2.IMREAD_COLOR)
    img_mask = img.copy()
    inpaintMask = np.zeros(img.shape[:2], np.uint8)

    # Variables to store times for the final plot
    ttime, ntime = 0, 0

    print("Instructions:")
    print(" - Draw on the image to create a mask (Green lines)")
    print(" - Press 't' for Telea Inpainting")
    print(" - Press 'n' for Navier-Stokes Inpainting")
    print(" - Press 'r' to Reset")
    print(" - Press 'ESC' to Exit and view performance graph")

    sketch = Sketcher('image', [img_mask, inpaintMask], lambda: ((0, 255, 0), 255))

    while True:
        ch = cv2.waitKey(1)
        if ch == 27: # ESC key
            break
        if ch == ord('t'):
            t1t = time.time()
            res = cv2.inpaint(src=img_mask, inpaintMask=inpaintMask, inpaintRadius=3, flags=cv2.INPAINT_TELEA)
            ttime = time.time() - t1t
            cv2.imshow('Inpaint Output using FMM', res)
            print(f"Telea Time: {ttime:.4f}s")
        if ch == ord('n'):
            t1n = time.time()
            res = cv2.inpaint(src=img_mask, inpaintMask=inpaintMask, inpaintRadius=3, flags=cv2.INPAINT_NS)
            ntime = time.time() - t1n
            cv2.imshow('Inpaint Output using NS Technique', res)
            print(f"NS Time: {ntime:.4f}s")
        if ch == ord('r'):
            img_mask[:] = img
            inpaintMask[:] = 0
            sketch.show()

    cv2.destroyAllWindows()

    # 2. Performance Comparison Plot
    if ttime > 0 or ntime > 0:
        times = [ttime, ntime]
        methods = ['INPAINT_TELEA', 'INPAINT_NS']
        plt.figure(figsize=(8, 6))
        plt.bar(methods, times, color=['blue', 'orange'], width=0.4)
        plt.xlabel('Algorithms')
        plt.ylabel('Runtime (seconds)')
        plt.title('Inpainting Runtime Comparison')
        plt.show()