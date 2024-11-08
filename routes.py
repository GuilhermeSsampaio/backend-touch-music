
from fastapi import APIRouter
import requests
import os

router = APIRouter()

url = "https://blob.squarecloud.app/v1/objects"
headers = {"Authorization": os.getenv('SQUARECLOUD_API_KEY')}

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

@router.get("/")
def home():
    return "home"

@router.get("/objetos")
def get_objetos():
    return objetos

@router.get("/objetos/{objeto_id}")    
def get_objetos_by_id(objeto_id: str):
    try:
        return objetos["response"]["objects"][objeto_id]
    except (KeyError, TypeError) as e:
        return {"error": f"Objeto não encontrado: {e}"}