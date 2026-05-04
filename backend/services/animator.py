# backend/services/animator.py
import os
import base64
import time
import io
import asyncio
from pathlib import Path
from PIL import Image, ImageOps
import replicate
from dotenv import load_dotenv


# ─── Load .env permanently ────────────────────────────────────────────────────
BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(dotenv_path=BASE_DIR / ".env", override=True)
# ─────────────────────────────────────────────────────────────────────────────

RESULTS_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "results"))
TEMP_DIR    = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "temp"))
os.makedirs(RESULTS_DIR, exist_ok=True)
os.makedirs(TEMP_DIR,    exist_ok=True)

MAX_RETRIES       = 2    # fewer retries — each one already has a timeout
RETRY_DELAY       = 2    # seconds between retries
REPLICATE_TIMEOUT = 60   # seconds to wait for Replicate before giving up


def get_token():
    """Always read fresh token — never cached."""
    token = os.environ.get("REPLICATE_API_TOKEN", "")
    if not token:
        load_dotenv(dotenv_path=BASE_DIR / ".env", override=True)
        token = os.environ.get("REPLICATE_API_TOKEN", "")
    if not token:
        raise Exception("REPLICATE_API_TOKEN not set! Check your backend/.env file")
    return token


def compress_image(input_path: str, max_size: int = 512) -> bytes:
    """
    Compress and resize image before sending to Replicate.
    Smaller size = faster upload + faster model processing.
    """
    img = Image.open(input_path).convert("RGB")
    if img.width > max_size or img.height > max_size:
        img.thumbnail((max_size, max_size), Image.LANCZOS)
        print(f" Resized image to {img.width}x{img.height}")
    buffer = io.BytesIO()
    img.save(buffer, format="JPEG", quality=78)  # slightly lower quality = faster transfer
    compressed = buffer.getvalue()
    original_size = os.path.getsize(input_path)
    print(f" Compressed: {original_size // 1024}KB → {len(compressed) // 1024}KB")
    return compressed


def animate_placeholder(input_path: str, output_name: str) -> str:
    """Placeholder animation function (kept for compatibility)."""
    with Image.open(input_path) as im:
        im = im.convert("RGB")
        mirrored = ImageOps.mirror(im)
        w, h = im.size
        new = Image.new("RGB", (w * 2, h))
        new.paste(im, (0, 0))
        new.paste(mirrored, (w, 0))
        if new.width > 1200:
            new = new.resize((1200, int(new.height * 1200 / new.width)))
        out_path = os.path.join(RESULTS_DIR, output_name)
        new.save(out_path, format="PNG", optimize=True)
    return out_path


def _run_replicate_sync(image_data_uri: str, token: str) -> bytes:
    """
    Blocking Replicate call — runs inside a thread via asyncio.to_thread
    so it never blocks the FastAPI event loop.
    """
    client = replicate.Client(api_token=token)
    output = client.run(
        "fofr/expression-editor:bf913bc90e1c44ba288ba3942a538693b72e8cc7df576f3beebe56adc0a92b86",
        input={
            "image":          image_data_uri,
            "smile":          0.9,
            "eyebrow":        0.1,
            "wink":           0,
            "pupil_x":        0,
            "pupil_y":        0,
            "aaa":            0,
            "eee":            0,
            "woo":            0,
            "rotate_pitch":   0,
            "rotate_yaw":     0,
            "rotate_roll":    0,
            "blink":          0,
            "output_format":  "webp",
            "output_quality": 90,
        }
    )
    if not output or len(output) == 0:
        raise Exception("Empty output from Replicate model")
    result_bytes = output[0].read()
    if not result_bytes:
        raise Exception("Empty bytes from Replicate model")
    return result_bytes


async def generate_smile_animation(input_path: str, output_filename: str) -> str:
    """
    Generate AI smile via Replicate with:
      - Non-blocking async execution (asyncio.to_thread)
      - Per-attempt timeout (REPLICATE_TIMEOUT seconds)
      - Automatic retry (MAX_RETRIES attempts)
      - Original-image fallback if all attempts fail
    """
    print(" Starting AI smile generation via Replicate...")

    token          = get_token()
    image_bytes    = compress_image(input_path, max_size=512)
    image_data_uri = f"data:image/jpeg;base64,{base64.b64encode(image_bytes).decode()}"

    for attempt in range(1, MAX_RETRIES + 1):
        try:
            print(f" Attempt {attempt}/{MAX_RETRIES} (timeout={REPLICATE_TIMEOUT}s)...")

            result_bytes = await asyncio.wait_for(
                asyncio.to_thread(_run_replicate_sync, image_data_uri, token),
                timeout=REPLICATE_TIMEOUT,
            )

            name       = Path(output_filename).stem
            final_path = os.path.join(TEMP_DIR, f"{name}.webp")
            with open(final_path, "wb") as f:
                f.write(result_bytes)

            print(f" AI smile saved on attempt {attempt}: {final_path}")
            return final_path

        except asyncio.TimeoutError:
            print(f" Attempt {attempt} timed out after {REPLICATE_TIMEOUT}s")
        except Exception as e:
            print(f" Attempt {attempt} failed: {e}")

        if attempt < MAX_RETRIES:
            print(f" Retrying in {RETRY_DELAY}s...")
            await asyncio.sleep(RETRY_DELAY)  # non-blocking sleep

    print(" All attempts failed. Returning original image.")
    return await _save_original(input_path, output_filename)


async def _save_original(input_path: str, output_filename: str) -> str:
    """Last resort: return a copy of the original image using Pillow."""
    img        = Image.open(input_path).convert("RGB")
    name       = Path(output_filename).stem
    final_path = os.path.join(TEMP_DIR, f"{name}.jpg")
    img.save(final_path, format="JPEG", quality=95)
    print(f" Saved original as fallback: {final_path}")
    return final_path


# ─── Aliases ──────────────────────────────────────────────────────────────────
async def generate_smile_with_opencv(input_path: str, output_filename: str) -> str:
    return await generate_smile_animation(input_path, output_filename)

async def generate_simple_smile(input_path: str, output_filename: str) -> str:
    return await generate_smile_animation(input_path, output_filename)