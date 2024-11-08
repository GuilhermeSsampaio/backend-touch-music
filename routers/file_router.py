
from fastapi import APIRouter, File, UploadFile
import os
import shutil

router = APIRouter()

UPLOAD_DIRECTORY = "uploads"

@router.post("/create_file")
async def create_file(file: bytes = File(...)):
    return {"file_size": len(file)}

@router.post("/uploadfile")
async def create_upload_file(file: UploadFile = File(...)):
    file_location = f"{UPLOAD_DIRECTORY}/{file.filename}"
    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    return {"info": f"file '{file.filename}' saved at '{file_location}'"}