from fastapi import FastAPI
from routers.enhance import router as enhance_router
from routers.animate import router as animate_router
from routers.video import router as video_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "Deep Nostalgia API running"}

app.include_router(enhance_router)
app.include_router(animate_router)
app.include_router(video_router)




