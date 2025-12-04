# backend/routers/enhance.py
from fastapi import APIRouter, UploadFile, File, Query
from fastapi.responses import FileResponse
from PIL import Image, ImageEnhance
import io
import os

router = APIRouter()

# Optional: create a results folder if it doesn't exist
RESULTS_DIR = os.path.join(os.path.dirname(__file__), "../results")
os.makedirs(RESULTS_DIR, exist_ok=True)

@router.post("/api/enhance/")
async def enhance(file: UploadFile = File(...), level: float = Query(50, ge=0, le=100)):
    """
    Enhance uploaded image based on user-selected level (0-100).
    """
    # Read image
    image = Image.open(io.BytesIO(await file.read()))
    
    # Convert level 0-100 to enhancement factor (1.0 = original, 2.0 = max)
    factor = 1 + (level / 100)
    
    # Apply sharpness enhancement (you can add clarity, contrast later)
    enhancer = ImageEnhance.Sharpness(image)
    image = enhancer.enhance(factor)
    
    # Save enhanced image to results folder
    output_filename = f"enhanced_{file.filename}"
    output_path = os.path.join(RESULTS_DIR, output_filename)
    image.save(output_path)

    # Return the image via FileResponse
    return FileResponse(output_path, media_type="image/png", filename=output_filename)



