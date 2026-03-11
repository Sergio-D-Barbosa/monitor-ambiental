from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {"status": "Projeto 02 - Monitor de Impacto Ambiental Ativo"}