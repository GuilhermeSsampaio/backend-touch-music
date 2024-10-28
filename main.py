from fastapi import FastAPI
import requests
from dotenv import load_dotenv
import os

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

# Obtém a API key do ambiente
api_key = os.getenv('SQUARECLOUD_API_KEY')
if not api_key:
    raise ValueError("SQUARECLOUD_API_KEY não encontrada nas variáveis de ambiente")

app = FastAPI()

url = "https://blob.squarecloud.app/v1/objects"

headers = {"Authorization": api_key}

# Função para buscar objetos da API
def fetch_objects():
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Levanta exceção para status codes de erro
        return response.json()
    except requests.RequestException as e:
        print(f"Erro ao buscar objetos: {e}")
        return {"error": "Falha ao buscar objetos"}

# Busca inicial dos objetos
objetos = fetch_objects()

@app.get("/")
def home():
    return "home"

@app.get("/objetos")
def get_objetos():
    return objetos

@app.get("/objetos/{objeto_id}")    
def get_objetos_by_id(objeto_id: str):
    try:
        return objetos["response"]["objects"][objeto_id]
    except (KeyError, TypeError) as e:
        return {"error": f"Objeto não encontrado: {e}"}

