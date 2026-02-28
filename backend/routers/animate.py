# backend/routers/animate.py
from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
import os
import shutil
from pathlib import Path

from backend.services import animator

router = APIRouter()


@router.post("/api/animate")
async def animate_image(file: UploadFile = File(...)):
    if not file.filename:
        raise HTTPException(status_code=400, detail="No filename provided")

    temp_dir = os.path.join(os.path.dirname(__file__), "..", "temp")
    temp_dir = os.path.abspath(temp_dir)
    os.makedirs(temp_dir, exist_ok=True)

    input_path = os.path.join(temp_dir, file.filename)
    with open(input_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    name, ext = os.path.splitext(file.filename)
    out_filename = f"animated_{name}.png"

    out_path = animator.animate_placeholder(input_path, out_filename)

    return FileResponse(
        out_path,
        media_type="image/png",
        filename=out_filename
    )


@router.post("/api/animate/smile")
async def generate_smile(file: UploadFile = File(...)):
    """
    Generate real AI smile using Replicate (with retry logic).
    Falls back to OpenCV only if Replicate fails 3 times.
    """
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

        name, ext = os.path.splitext(file.filename)
        out_filename = f"smile_{name}"

        print(f"📥 Processing: {file.filename}")

        # ── ALWAYS call Replicate AI first (with retry) ──────────────────────
        out_path = await animator.generate_smile_animation(
            input_path, out_filename
        )

        # ── Detect output format (Replicate returns webp, OpenCV returns jpg) 
        out_ext = Path(out_path).suffix.lower()
        media_type = "image/webp" if out_ext == ".webp" else "image/jpeg"
        download_name = f"{out_filename}{out_ext}"

        print(f"✅ Returning: {out_path} as {media_type}")

        return FileResponse(
            out_path,
            media_type=media_type,
            filename=download_name
        )

    except Exception as e:
        print(f"❌ Error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        # Clean up input file
        if os.path.exists(input_path):
            try:
                os.remove(input_path)
            except:
                pass