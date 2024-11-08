from fastapi import APIRouter, File, UploadFile, HTTPException
import os
import shutil
import speech_recognition as sr
from pydub import AudioSegment
import logging
import librosa
import numpy as np

router = APIRouter()

UPLOAD_DIRECTORY = "uploads"

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

def extract_pitch(file_path: str) -> str:
    try:
        y, sr = librosa.load(file_path)
        pitches, magnitudes = librosa.core.piptrack(y=y, sr=sr)
        
        # Coletar todos os pitches detectados com magnitude significativa
        detected_pitches = []
        for t in range(pitches.shape[1]):
            index = magnitudes[:, t].argmax()
            pitch = pitches[index, t]
            if pitch > 0:  # Ignorar valores zero
                detected_pitches.append(pitch)
        
        # Garantir que temos pitches suficientes para analisar
        if not detected_pitches:
            raise ValueError("Não foi possível detectar o tom da música")
        
        # Calcular a moda para encontrar o pitch mais comum
        pitch = np.median(detected_pitches)
        note = librosa.hz_to_note(pitch)
        return note
    except Exception as e:
        logging.exception("Erro ao extrair o tom da música")
        raise HTTPException(status_code=500, detail=f"Erro ao extrair o tom da música: {str(e)}")


@router.post("/process_audio")
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

        # Extração do tom da música
        note = extract_pitch(converted_file_location)
    except (sr.UnknownValueError, sr.RequestError, ValueError) as e:
        raise HTTPException(status_code=500, detail=f"Erro ao processar o áudio: {str(e)}")
    
    return {
        "text": text,
        "note": note
    }