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
    image = Image.open(io.BytesIO(await file.read()))

    # -----------------------------
    # 1️⃣ Enhancement (brightness/contrast)
    factor_enh = 1 + (enh / 100)
    enhancer = ImageEnhance.Contrast(image)
    image = enhancer.enhance(factor_enh)

    # -----------------------------
    # 2️⃣ Sharpness
    factor_sharp = 1 + (sharp / 100)
    enhancer = ImageEnhance.Sharpness(image)
    image = enhancer.enhance(factor_sharp)

    # -----------------------------
    # 3️⃣ Clarity (simple filter to simulate clarity)
    factor_clarity = clarity / 100
    if factor_clarity > 0:
        image = image.filter(ImageFilter.DETAIL)

    # -----------------------------
    # Convert to base64
    buffer = io.BytesIO()
    image.save(buffer, format="PNG")
    img_bytes = buffer.getvalue()
    base64_img = base64.b64encode(img_bytes).decode("utf-8")

    return {"image": base64_img}
