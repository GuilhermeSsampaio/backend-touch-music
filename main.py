from fastapi import FastAPI
from dotenv import load_dotenv
import os
from routes import router

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

# Obtém a API key do ambiente
api_key = os.getenv('SQUARECLOUD_API_KEY')
if not api_key:
    raise ValueError("SQUARECLOUD_API_KEY não encontrada nas variáveis de ambiente")

app = FastAPI()

app.include_router(router)

