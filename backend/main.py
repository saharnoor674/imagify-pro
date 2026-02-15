# backend/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
import os

# import routers
from backend.routers import enhance  # existing
from backend.routers import animate  # new
from backend.routers import video    # if exists

app = FastAPI()

# CORS - allow frontend (adjust origins for production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "Deep Nostalgia API running"}

# include routers
app.include_router(enhance.router)
app.include_router(animate.router)
# if video router exists:
# app.include_router(video.router)

# results serving
RESULTS_DIR = os.path.join(os.path.dirname(__file__), "results")
RESULTS_DIR = os.path.abspath(RESULTS_DIR)

@app.get("/results/{filename}")
def get_result(filename: str):
    path = os.path.join(RESULTS_DIR, filename)
    if not os.path.exists(path):
        return {"detail": "file not found"}
    return FileResponse(path)
# backend/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
import os

# import routers
from backend.routers import enhance  # existing
from backend.routers import animate  # new
from backend.routers import video    # if exists

app = FastAPI()

# CORS - allow frontend (adjust origins for production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "Deep Nostalgia API running"}

# include routers
app.include_router(enhance.router)
app.include_router(animate.router)
# if video router exists:
# app.include_router(video.router)

# results serving
RESULTS_DIR = os.path.join(os.path.dirname(__file__), "results")
RESULTS_DIR = os.path.abspath(RESULTS_DIR)

@app.get("/results/{filename}")
def get_result(filename: str):
    path = os.path.join(RESULTS_DIR, filename)
    if not os.path.exists(path):
        return {"detail": "file not found"}
    return FileResponse(path)


# ADD THIS AT THE BOTTOM:
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)





