#!/bin/bash

# Criação e ativação do ambiente virtual
python3.12 -m venv venv
source venv/bin/activate

# Instalação das dependências
pip install -r requirements.txt

# Executa o servidor com uvicorn, usando a porta 8000 se $PORT não estiver definida
uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000}
