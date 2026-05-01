# backend/main.py
import sys
import os

# Fix imports for both local and Railway
sys.path.insert(0, os.path.dirname(__file__))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse

from routers import enhance
from routers import animate
from routers import video

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "Imagify-Pro API running"}

app.include_router(enhance.router)
app.include_router(animate.router)
app.include_router(video.router)

RESULTS_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "results"))

@app.get("/results/{filename}")
def get_result(filename: str):
    path = os.path.join(RESULTS_DIR, filename)
    if not os.path.exists(path):
        return {"detail": "file not found"}
    return FileResponse(path)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)