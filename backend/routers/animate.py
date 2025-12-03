# backend/routers/animate.py
from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
import os
import shutil
from backend.services import animator


router = APIRouter()

@router.post("/api/animate")
async def animate_image(file: UploadFile = File(...)):
    # basic validation
    if not file.filename:
        raise HTTPException(status_code=400, detail="No filename provided")

    # save uploaded file to a temp path
    temp_dir = os.path.join(os.path.dirname(__file__), "..", "temp")
    temp_dir = os.path.abspath(temp_dir)
    os.makedirs(temp_dir, exist_ok=True)

    input_path = os.path.join(temp_dir, file.filename)
    with open(input_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # create output filename
    name, ext = os.path.splitext(file.filename)
    out_filename = f"animated_{name}.png"  # normalized to .png

    # call placeholder animator
    out_path = animator.animate_placeholder(input_path, out_filename)

    # return relative URL for the frontend / browser
    url = f"/results/{out_filename}"
    return JSONResponse(status_code=200, content={"message": "Animation successful", "result_url": url})

