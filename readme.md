# Projeto FastAPI

Este é um projeto de exemplo usando FastAPI para criar uma API simples.

## Pré-requisitos

- Python 3.7 ou superior
- pip (gerenciador de pacotes do Python)

## Instalação

### Windows

1. Clone o repositório:
   ```sh
   git clone https://github.com/seu-usuario/seu-repositorio.git
   cd seu-repositorio
   ```
2. Crie um ambiente virtual:
   ```sh
   python3 -m venv venv
   ```
3. Ative o ambiente virtual:
   ```sh
   source venv/bin/activate
   ```
4. Instale as dependências:
   ```sh
   pip install -r requirements.txt
   ```

### Linux

1. Clone o repositório:
   ```sh
   git clone https://github.com/seu-usuario/seu-repositorio.git
   cd seu-repositorio
   ```
2. Crie um ambiente virtual:
   ```sh
   python3 -m venv venv
   ```
3. Ative o ambiente virtual:
   ```sh
   source venv/bin/activate
   ```
4. Instale as dependências:
   ```sh
   pip install -r requirements.txt
   ```

## Configuração

Crie um arquivo `.env` na raiz do projeto e adicione suas variáveis de ambiente:

```
URL=https://blob.squarecloud.app/v1/objects
518AUTHORIZATION=ed0262c96560c19e17a459bad487451640343-da78c4413490d9ce905b7a09eeb552ee3f4c5aed0fa876d45c85cac98b60d166
```

## Executando o Projeto

Certifique-se de que o ambiente virtual está ativado.

Execute o servidor:

```sh
uvicorn main:app --reload
```

## Endpoints

- `GET /`: Retorna uma mensagem de boas-vindas.
- `GET /objetos`: Retorna a lista de objetos.
- `GET /objetos/{objeto_id}`: Retorna um objeto específico pelo ID.

## Licença

Este projeto está licenciado sob os termos da licença MIT.
