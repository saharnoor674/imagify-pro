# backend/services/animator.py
import os
import shutil
from PIL import Image, ImageOps

RESULTS_DIR = os.path.join(os.path.dirname(__file__), "..", "results")
RESULTS_DIR = os.path.abspath(RESULTS_DIR)
os.makedirs(RESULTS_DIR, exist_ok=True)

def animate_placeholder(input_path: str, output_name: str) -> str:
    """
    Placeholder animation function.
    Currently: creates a slightly modified copy of the input image
    (converts to RGB + adds a subtle mirror + small border) and saves
    it as the "animated" result.
    Replace this function later with real animation model code.
    Returns absolute output path.
    """
    with Image.open(input_path) as im:
        # ensure RGB
        im = im.convert("RGB")
        # create a mirrored side-by-side image to simulate 'effect'
        mirrored = ImageOps.mirror(im)
        w, h = im.size
        new = Image.new("RGB", (w * 2, h))
        new.paste(im, (0, 0))
        new.paste(mirrored, (w, 0))

        # optional: resize moderately if too large
        max_w = 1200
        if new.width > max_w:
            new = new.resize((max_w, int(new.height * max_w / new.width)))

        out_path = os.path.join(RESULTS_DIR, output_name)
        new.save(out_path, format="PNG", optimize=True)
    return out_path
