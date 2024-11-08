from fastapi import FastAPI
import os

from routers import file_router, audio_router

app = FastAPI()

UPLOAD_DIRECTORY = "uploads"

if not os.path.exists(UPLOAD_DIRECTORY):
    os.makedirs(UPLOAD_DIRECTORY)

app.include_router(file_router.router)
app.include_router(audio_router.router)

@app.get("/")
def home():
    return {"message": "Hello World"}