from fastapi import APIRouter, UploadFile, File
from backend.services.enhancer import enhance_image

router = APIRouter()

@router.post("/api/enhance/")
async def enhance(file: UploadFile = File(...)):
    image_bytes = await file.read()
    enhanced_image = enhance_image(image_bytes)
    return {"status": "success", "image": enhanced_image.hex()}  # convert bytes to hex string


