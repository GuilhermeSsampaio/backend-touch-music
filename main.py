from fastapi import FastAPI, File, UploadFile, HTTPException  # Importando HTTPException correto
import os
import shutil
import speech_recognition as sr
import librosa
import numpy as np

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

@app.post("/process_audio")
async def process_audio(filename: str):
    file_location = f"{UPLOAD_DIRECTORY}/{filename}" 
    
    if not os.path.exists(file_location):
        raise HTTPException(status_code=404, detail="File not found")
    
    if not file_location.endswith(('.wav', '.flac', '.ogg', '.au', '.mp3')):
        raise HTTPException(status_code=400, detail="Formato de arquivo não suportado")

    
    # Reconhecimento de fala
    recognizer = sr.Recognizer()
    with sr.AudioFile(file_location) as source:
        audio = recognizer.record(source)
        text = recognizer.recognize_google(audio, language="pt-BR")
        
    # Análise de áudio com librosa
    y, sample_rate = librosa.load(file_location)
    tempo, beat_frames = librosa.beat.beat_track(y=y, sr=sample_rate)
    chroma = librosa.feature.chroma_cqt(y=y, sr=sample_rate)
    
    # Estimação de acordes (simplificada)
    chords = librosa.decompose.decompose(chroma, n_components=8)
    
    return {
        "text": text,
        "tempo": tempo,
        "chroma_shape": chroma.shape,
        "chords": chords.tolist()
    }
