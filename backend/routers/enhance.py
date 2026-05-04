import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from fastapi import APIRouter, UploadFile, File, Query
from PIL import Image, ImageEnhance, ImageFilter
import io
import base64

router = APIRouter()

@router.post("/api/enhance/")
async def enhance(
    file: UploadFile = File(...),
    enh: float = Query(50, ge=0, le=100),
    sharp: float = Query(50, ge=0, le=100),
    clarity: float = Query(50, ge=0, le=100)
):
    image = Image.open(io.BytesIO(await file.read())).convert("RGB")

    # ─── 1. BRIGHTNESS ───────────────────────────────────────────────────────
    if enh != 50:
        brightness_factor = 1.0 + (enh - 50) * 0.008
        image = ImageEnhance.Brightness(image).enhance(brightness_factor)

    # ─── 2. CONTRAST ─────────────────────────────────────────────────────────
    if enh != 50:
        contrast_factor = 1.0 + (enh - 50) * 0.012
        image = ImageEnhance.Contrast(image).enhance(contrast_factor)

    # ─── 3. VIBRANCE (via Pillow Color enhancer) ─────────────────────────────
    if enh != 50:
        vibrance_factor = 1.0 + (enh - 50) * 0.006
        image = ImageEnhance.Color(image).enhance(max(0.0, vibrance_factor))

    # ─── 4. SHARPNESS ────────────────────────────────────────────────────────
    if sharp != 50:
        sharp_factor = 1.0 + (sharp - 50) * 0.06
        image = ImageEnhance.Sharpness(image).enhance(max(0.0, sharp_factor))

    # ─── 5. CLARITY (multi-pass unsharp via Pillow filters) ──────────────────
    if clarity != 50:
        passes = int(1 + (abs(clarity - 50) / 25))  # 1–3 passes based on strength
        for _ in range(passes):
            image = image.filter(ImageFilter.UnsharpMask(
                radius=2,
                percent=int((clarity - 50) * 3),
                threshold=2
            ))

        if clarity > 70:
            image = image.filter(ImageFilter.SHARPEN)
            image = image.filter(ImageFilter.DETAIL)
        if clarity > 85:
            image = image.filter(ImageFilter.SHARPEN)

    # ─── 6. NOISE REDUCTION ──────────────────────────────────────────────────
    if enh > 70 or sharp > 70 or clarity > 70:
        image = image.filter(ImageFilter.SMOOTH)

    # ─── Convert to Base64 ───────────────────────────────────────────────────
    buffer = io.BytesIO()
    image.save(buffer, format="PNG", optimize=True)
    base64_img = base64.b64encode(buffer.getvalue()).decode("utf-8")

    return {
        "status": "success",
        "image": base64_img,
        "settings": {
            "enhancement": enh,
            "sharpness": sharp,
            "clarity": clarity
        }
    }