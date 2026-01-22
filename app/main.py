from fastapi import FastAPI
from app.database.core import engine, Base
from app.routes import manutencao, material 

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Backend Challenge API")

app.include_router(manutencao.router)
app.include_router(material.router) 

@app.get("/")
def health():
    return {"status": "ok"}