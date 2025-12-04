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
