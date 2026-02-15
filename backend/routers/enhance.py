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
    # Read image
    image = Image.open(io.BytesIO(await file.read())).convert("RGB")

    # -----------------------------
    # 1️⃣ Brightness
    brightness_factor = 1 + (enh - 50) / 100
    image = ImageEnhance.Brightness(image).enhance(brightness_factor)

    # -----------------------------
    # 2️⃣ Contrast
    contrast_factor = 1 + (enh - 50) / 80
    image = ImageEnhance.Contrast(image).enhance(contrast_factor)

    # -----------------------------
    # 3️⃣ Color (Vibrance)
    color_factor = 1 + (enh - 50) / 70
    image = ImageEnhance.Color(image).enhance(color_factor)

    # -----------------------------
    # 4️⃣ Sharpness
    sharp_factor = 1 + sharp / 60
    image = ImageEnhance.Sharpness(image).enhance(sharp_factor)

    # -----------------------------
    # 5️⃣ Clarity (real visible effect)
    if clarity > 30:
        image = image.filter(ImageFilter.SHARPEN)

    if clarity > 70:
        image = image.filter(ImageFilter.DETAIL)

    # -----------------------------
    # Convert to Base64
    buffer = io.BytesIO()
    image.save(buffer, format="PNG")
    base64_img = base64.b64encode(buffer.getvalue()).decode("utf-8")

    return {
        "status": "success",
        "image": base64_img
    }
