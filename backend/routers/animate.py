from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
import os
import shutil

from backend.services import animator

router = APIRouter()

@router.post("/api/animate")
async def animate_image(file: UploadFile = File(...)):
    if not file.filename:
        raise HTTPException(status_code=400, detail="No filename provided")

    # Save uploaded file temporarily
    temp_dir = os.path.join(os.path.dirname(__file__), "..", "temp")
    temp_dir = os.path.abspath(temp_dir)
    os.makedirs(temp_dir, exist_ok=True)

    input_path = os.path.join(temp_dir, file.filename)
    with open(input_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # output file
    name, ext = os.path.splitext(file.filename)
    out_filename = f"animated_{name}.png"

    # Generate animated image
    out_path = animator.animate_placeholder(input_path, out_filename)

    # Return actual file to frontend
    return FileResponse(
        out_path,
        media_type="image/png",
        filename=out_filename
    )

@router.post("/api/animate/smile")
async def generate_smile(file: UploadFile = File(...)):
    """Generate smile effect on face image (FREE VERSION)"""
    if not file.filename:
        raise HTTPException(status_code=400, detail="No filename provided")
    
    # Validate file type
    allowed_extensions = {'.jpg', '.jpeg', '.png', '.webp', '.jfif'}
    file_ext = os.path.splitext(file.filename)[1].lower()
    if file_ext not in allowed_extensions:
        raise HTTPException(
            status_code=400, 
            detail=f"Invalid file type. Allowed: {', '.join(allowed_extensions)}"
        )

    # Save uploaded file
    temp_dir = os.path.join(os.path.dirname(__file__), "..", "temp")
    temp_dir = os.path.abspath(temp_dir)
    os.makedirs(temp_dir, exist_ok=True)
    input_path = os.path.join(temp_dir, file.filename)
    
    try:
        with open(input_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Generate output filename
        name, ext = os.path.splitext(file.filename)
        out_filename = f"smile_{name}"

        print(f"📥 Processing: {file.filename}")

        # Try OpenCV version first, fallback to simple version
        try:
            out_path = await animator.generate_smile_with_opencv(input_path, out_filename)
        except:
            out_path = await animator.generate_smile_animation(input_path, out_filename)

        # Return image (not video for free version)
        return FileResponse(
            out_path,
            media_type="image/jpeg",
            filename=f"{out_filename}.jpg"
        )
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
    
    finally:
        # Clean up
        if os.path.exists(input_path):
            try:
                os.remove(input_path)
            except:
                pass