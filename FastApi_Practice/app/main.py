from fastapi import FastAPI
from app.rutas import usuarios,productos
app = FastAPI()

app.include_router(usuarios.router)
app.include_router(productos.router)

@app.get("/")
def home():
    return {"msg":"Hola FastAPI"}

@app.get("/saludo")
def saludo():
    return {"mgs":"Buenos días"}

@app.get("/despedida")
def despedida():
    return {"msg":"Chao"}
