from fastapi import APIRouter, UploadFile, File, Query
from PIL import Image, ImageEnhance, ImageFilter
import io
import base64
import numpy as np

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

    # ─── 1. BRIGHTNESS ───────────────────────────────────────────────────────
    if enh != 50:
        brightness_factor = 1.0 + (enh - 50) * 0.008
        image = ImageEnhance.Brightness(image).enhance(brightness_factor)

    # ─── 2. CONTRAST ─────────────────────────────────────────────────────────
    if enh != 50:
        contrast_factor = 1.0 + (enh - 50) * 0.012
        image = ImageEnhance.Contrast(image).enhance(contrast_factor)

    # ─── 3. VIBRANCE ─────────────────────────────────────────────────────────
    if enh != 50:
        img_array = np.array(image, dtype=np.float32)
        r, g, b = img_array[:,:,0], img_array[:,:,1], img_array[:,:,2]
        max_c = np.maximum(np.maximum(r, g), b)
        min_c = np.minimum(np.minimum(r, g), b)
        saturation = (max_c - min_c) / (max_c + 1e-6)
        vibrance_strength = (enh - 50) * 0.006
        vibrance_mask = (1.0 - saturation) * vibrance_strength
        img_array[:,:,0] = np.clip(r + (r - (g + b) / 2) * vibrance_mask, 0, 255)
        img_array[:,:,1] = np.clip(g + (g - (r + b) / 2) * vibrance_mask, 0, 255)
        img_array[:,:,2] = np.clip(b + (b - (r + g) / 2) * vibrance_mask, 0, 255)
        image = Image.fromarray(img_array.astype(np.uint8))

    # ─── 4. SHARPNESS (Unsharp Mask) ─────────────────────────────────────────
    if sharp != 50:
        img_array = np.array(image, dtype=np.float32)
        blurred = image.filter(ImageFilter.GaussianBlur(radius=1.2))
        blur_array = np.array(blurred, dtype=np.float32)
        sharp_strength = (sharp - 50) * 0.06
        sharpened = img_array + (img_array - blur_array) * sharp_strength
        image = Image.fromarray(np.clip(sharpened, 0, 255).astype(np.uint8))

    # ─── 5. CLARITY (Full Deblur - removes blur completely) ──────────────────
    if clarity != 50:
        img_array = np.array(image, dtype=np.float32)

        # 3 levels of detail recovery
        blur_fine   = np.array(image.filter(ImageFilter.GaussianBlur(radius=1)), dtype=np.float32)
        blur_mid    = np.array(image.filter(ImageFilter.GaussianBlur(radius=3)), dtype=np.float32)
        blur_coarse = np.array(image.filter(ImageFilter.GaussianBlur(radius=6)), dtype=np.float32)

        clarity_strength = (clarity - 50) * 0.07

        fine_detail   = (img_array - blur_fine)   * clarity_strength * 1.5
        mid_detail    = (img_array - blur_mid)     * clarity_strength * 1.0
        coarse_detail = (img_array - blur_coarse)  * clarity_strength * 0.5

        clarified = img_array + fine_detail + mid_detail + coarse_detail
        image = Image.fromarray(np.clip(clarified, 0, 255).astype(np.uint8))

        # Extra deblur passes for high clarity values
        if clarity > 70:
            image = image.filter(ImageFilter.SHARPEN)
            image = image.filter(ImageFilter.DETAIL)
        if clarity > 85:
            image = image.filter(ImageFilter.SHARPEN)

    # ─── 6. NOISE REDUCTION (auto when heavy settings) ───────────────────────
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