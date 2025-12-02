from fastapi import APIRouter, UploadFile, File

router = APIRouter()

@router.post("/api/animate")
async def animate_image(file: UploadFile = File(...)):
    # TODO: add your animation logic here
    return {"message": "Animation module working!", "filename": file.filename}
