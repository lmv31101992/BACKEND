import uvicorn
from fastapi import FastAPI
from routers import auth,register,delete

app = FastAPI()

app.include_router(auth.router)
app.include_router(register.router)
app.include_router(delete.router)

@app.get("/")
async def root():
    return "hola cliente, bienvenido a nuestra app"

if __name__=="__main__":
    uvicorn.run("main:app",port=8000 , reload=True,)