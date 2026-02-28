# backend/services/animator.py
import os
import base64
import time
from pathlib import Path
from PIL import Image, ImageOps
import cv2
import numpy as np
import replicate
from dotenv import load_dotenv

# ─── Load .env ────────────────────────────────────────────────────────────────
load_dotenv()
# ─────────────────────────────────────────────────────────────────────────────

RESULTS_DIR = os.path.join(os.path.dirname(__file__), "..", "results")
RESULTS_DIR = os.path.abspath(RESULTS_DIR)
os.makedirs(RESULTS_DIR, exist_ok=True)

TEMP_DIR = os.path.join(os.path.dirname(__file__), "..", "temp")
os.makedirs(TEMP_DIR, exist_ok=True)

# ─── Token ────────────────────────────────────────────────────────────────────
REPLICATE_TOKEN = os.environ.get("REPLICATE_API_TOKEN", "")
# ─────────────────────────────────────────────────────────────────────────────

MAX_RETRIES = 3       # retry up to 3 times
RETRY_DELAY = 4       # wait 4 seconds between retries


def animate_placeholder(input_path: str, output_name: str) -> str:
    """Placeholder animation function (kept for compatibility)."""
    with Image.open(input_path) as im:
        im = im.convert("RGB")
        mirrored = ImageOps.mirror(im)
        w, h = im.size
        new = Image.new("RGB", (w * 2, h))
        new.paste(im, (0, 0))
        new.paste(mirrored, (w, 0))
        max_w = 1200
        if new.width > max_w:
            new = new.resize((max_w, int(new.height * max_w / new.width)))
        out_path = os.path.join(RESULTS_DIR, output_name)
        new.save(out_path, format="PNG", optimize=True)
    return out_path


async def generate_smile_animation(input_path: str, output_filename: str) -> str:
    """
    Generate a REAL AI smile using Replicate API with retry logic.
    Retries up to 3 times before falling back to OpenCV.
    """
    print(" Starting AI smile generation via Replicate...")

    last_error = None

    # ── Retry loop ────────────────────────────────────────────────────────────
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            print(f" Attempt {attempt}/{MAX_RETRIES}...")
            result_path = await _replicate_smile(input_path, output_filename)
            print(f"Real AI smile generated on attempt {attempt}!")
            return result_path

        except Exception as e:
            last_error = e
            print(f"Attempt {attempt} failed: {e}")

            if attempt < MAX_RETRIES:
                print(f"Waiting {RETRY_DELAY}s before retry...")
                time.sleep(RETRY_DELAY)

    # ── All retries failed → fallback to OpenCV ───────────────────────────────
    print(f" All {MAX_RETRIES} attempts failed. Using OpenCV fallback...")
    return await _opencv_smile_fallback(input_path, output_filename)


async def _replicate_smile(input_path: str, output_filename: str) -> str:
    """
    Use fofr/expression-editor on Replicate.
    Real AI model - produces natural photorealistic smiles.
    """
    print(" Connecting to Replicate API...")

    # Read and encode image
    with open(input_path, "rb") as f:
        image_bytes = f.read()

    suffix = Path(input_path).suffix.lower()
    mime_map = {
        ".jpg": "image/jpeg",
        ".jpeg": "image/jpeg",
        ".png": "image/png",
        ".webp": "image/webp",
    }
    mime_type = mime_map.get(suffix, "image/jpeg")
    base64_image = base64.b64encode(image_bytes).decode("utf-8")
    image_data_uri = f"data:{mime_type};base64,{base64_image}"

    print("Sending image to Replicate AI model...")

    # Create client with token
    client = replicate.Client(api_token=REPLICATE_TOKEN)

    # Run model
    output = client.run(
        "fofr/expression-editor:bf913bc90e1c44ba288ba3942a538693b72e8cc7df576f3beebe56adc0a92b86",
        input={
            "image": image_data_uri,
            "smile": 0.9,
            "eyebrow": 0.1,
            "wink": 0,
            "pupil_x": 0,
            "pupil_y": 0,
            "aaa": 0,
            "eee": 0,
            "woo": 0,
            "rotate_pitch": 0,
            "rotate_yaw": 0,
            "rotate_roll": 0,
            "blink": 0,
            "output_format": "webp",
            "output_quality": 95,
        }
    )

    print("Replicate returned result!")

    if not output or len(output) == 0:
        raise Exception("Empty output from Replicate model")

    # Read file object directly
    result_bytes = output[0].read()

    if not result_bytes:
        raise Exception("Empty bytes from Replicate model")

    # Save result
    name = Path(output_filename).stem
    final_path = os.path.join(TEMP_DIR, f"{name}.webp")

    with open(final_path, "wb") as f:
        f.write(result_bytes)

    print(f" Saved AI smile: {final_path}")
    return final_path


async def _opencv_smile_fallback(input_path: str, output_filename: str) -> str:
    """Fallback: OpenCV + MediaPipe smile."""
    try:
        import mediapipe as mp

        print("Using OpenCV fallback smile...")

        img = cv2.imread(input_path)
        if img is None:
            raise Exception("Could not read image")

        h, w, _ = img.shape

        mp_face_mesh = mp.solutions.face_mesh
        face_mesh = mp_face_mesh.FaceMesh(
            static_image_mode=True,
            max_num_faces=1,
            refine_landmarks=True,
            min_detection_confidence=0.5
        )

        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = face_mesh.process(img_rgb)

        if not results.multi_face_landmarks:
            print(" No face detected")
            return await _save_original(input_path, output_filename)

        landmarks = [
            (int(lm.x * w), int(lm.y * h))
            for lm in results.multi_face_landmarks[0].landmark
        ]

        result = _apply_smile_warp(img, landmarks)

        name = Path(output_filename).stem
        final_path = os.path.join(TEMP_DIR, f"{name}.jpg")
        cv2.imwrite(final_path, result, [cv2.IMWRITE_JPEG_QUALITY, 95])

        print(f" OpenCV smile saved: {final_path}")
        return final_path

    except Exception as e:
        print(f"❌ OpenCV fallback failed: {e}")
        return await _save_original(input_path, output_filename)


def _apply_smile_warp(img, landmarks):
    """Clean OpenCV smile warp."""
    h, w = img.shape[:2]
    LEFT_CORNER = 61
    RIGHT_CORNER = 291
    UPPER_LIP_KEY = [185, 40, 37, 0, 267, 270, 409]

    left_corner = np.array(landmarks[LEFT_CORNER], dtype=np.float32)
    right_corner = np.array(landmarks[RIGHT_CORNER], dtype=np.float32)

    mouth_width = np.linalg.norm(right_corner - left_corner)
    smile_lift = int(mouth_width * 0.22)
    smile_spread = int(mouth_width * 0.04)
    radius = 18

    x_grid, y_grid = np.meshgrid(np.arange(w), np.arange(h))
    disp_x = np.zeros((h, w), dtype=np.float32)
    disp_y = np.zeros((h, w), dtype=np.float32)

    for corner, sign in [(left_corner, -1), (right_corner, 1)]:
        dist = np.sqrt((x_grid - corner[0])**2 + (y_grid - corner[1])**2)
        weight = np.exp(-(dist**2) / (2 * radius**2))
        disp_y -= smile_lift * weight
        disp_x += sign * smile_spread * weight

    for idx in UPPER_LIP_KEY:
        if idx < len(landmarks):
            pt = np.array(landmarks[idx], dtype=np.float32)
            dist = np.sqrt((x_grid - pt[0])**2 + (y_grid - pt[1])**2)
            weight = np.exp(-(dist**2) / (2 * (radius * 0.7)**2))
            disp_y -= (smile_lift * 0.25) * weight

    map_x = np.clip((x_grid + disp_x).astype(np.float32), 0, w - 1)
    map_y = np.clip((y_grid + disp_y).astype(np.float32), 0, h - 1)
    return cv2.remap(img, map_x, map_y, cv2.INTER_LINEAR, borderMode=cv2.BORDER_REPLICATE)


async def _save_original(input_path: str, output_filename: str) -> str:
    """Last resort: return original image."""
    img = cv2.imread(input_path)
    name = Path(output_filename).stem
    final_path = os.path.join(TEMP_DIR, f"{name}.jpg")
    cv2.imwrite(final_path, img, [cv2.IMWRITE_JPEG_QUALITY, 95])
    return final_path


# ─── Aliases ──────────────────────────────────────────────────────────────────
async def generate_smile_with_opencv(input_path: str, output_filename: str) -> str:
    return await generate_smile_animation(input_path, output_filename)

async def generate_simple_smile(input_path: str, output_filename: str) -> str:
    return await generate_smile_animation(input_path, output_filename)