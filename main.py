from fastapi import FastAPI, File, UploadFile, HTTPException  # Importando HTTPException correto
import os
import shutil
import speech_recognition as sr
from pydub import AudioSegment
import logging

app = FastAPI()

UPLOAD_DIRECTORY = "uploads"

if not os.path.exists(UPLOAD_DIRECTORY):
    os.makedirs(UPLOAD_DIRECTORY)

@app.get("/")
def home():
    return {"message": "Hello World"}

@app.post("/create_file")
async def create_file(file: bytes = File(...)):
    return {"file_size": len(file)}

@app.post("/uploadfile")
async def create_upload_file(file: UploadFile = File(...)):
    file_location = f"{UPLOAD_DIRECTORY}/{file.filename}"
    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    return {"info": f"file '{file.filename}' saved at '{file_location}'"}

def convert_audio(file_path: str, target_format: str = 'wav') -> str:
    try:
        # Verifica se o FFmpeg está instalado
        if not shutil.which("ffmpeg"):
            raise HTTPException(status_code=500, detail="FFmpeg não está instalado ou não está no PATH do sistema.")
        
        audio = AudioSegment.from_file(file_path)
        converted_file_path = f"{os.path.splitext(file_path)[0]}.{target_format}"
        audio.export(converted_file_path, format=target_format)
        return converted_file_path
    except Exception as e:
        logging.exception("Erro ao converter o arquivo de áudio")
        raise HTTPException(status_code=500, detail=f"Erro ao converter o arquivo de áudio: {str(e)}")

@app.post("/process_audio")
async def process_audio(file: UploadFile = File(...)):
    file_location = f"{UPLOAD_DIRECTORY}/{file.filename}"
    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    if not file_location.endswith(('.wav', '.flac', '.ogg', '.au', '.mp3')):
        raise HTTPException(status_code=400, detail="Formato de arquivo não suportado")

    try:
        # Converte o arquivo de áudio para WAV
        converted_file_location = convert_audio(file_location, 'wav')

        # Reconhecimento de fala
        recognizer = sr.Recognizer()
        with sr.AudioFile(converted_file_location) as source:
            audio = recognizer.record(source)
            text = recognizer.recognize_google(audio, language="pt-BR")
    except (sr.UnknownValueError, sr.RequestError, ValueError) as e:
        raise HTTPException(status_code=500, detail=f"Erro ao processar o áudio: {str(e)}")
    
    return {
        "text": text
    }
