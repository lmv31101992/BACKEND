from fastapi import FastAPI,HTTPException, Depends, APIRouter
from routers import register
from clases import Conexion,BaseDatos,Usuario
import uvicorn

access_list_bbdd = ['bd_pruebas', "postgres", 'admin', "127.0.0.1", "5432"]
conexion = Conexion(access_list_bbdd)
bbdd = BaseDatos()
u = Usuario()

def get_conexion_instance():
    return conexion

def get_bbdd_instance():
    return bbdd

def get_usuario_instance():
    return u


app = FastAPI()
print("1")
app.include_router(register.router, dependencies=[Depends(get_conexion_instance), Depends(get_bbdd_instance), Depends(get_usuario_instance)])
print("2")
@app.get("/")
async def root():
    return "hola cliente, bienvenido a nuestra app"

if __name__=="__main__":
    uvicorn.run("main:app",port=8000 , reload=True,)