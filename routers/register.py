from fastapi import APIRouter,status,HTTPException,Depends
from fastapi.security import OAuth2PasswordRequestForm
from helpers import usuario,conexion,basedatos

router = APIRouter()

@router.post("/register")
async def recurso(user:OAuth2PasswordRequestForm = Depends()):
    connect = conexion.abrirConexion(conexion.docker_list)
    if not connect:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Fallo en conexion con base de datos", 
            headers={"WWWW-Autenticate":"Bearer"})

    if user.username is None and user.password is None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Credenciales vacias", 
            headers={"WWWW-Autenticate":"Bearer"})
    conexion.crearTabla(connect,"credenciales")

    if basedatos.existeUsername(connect,"credenciales",user.username):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="USUARIO REGISTRADO!", 
            headers={"WWWW-Autenticate":"Bearer"})
    
    usr = [user.username,user.username,"",usuario.HashedPassword(user.password),False]
    basedatos.insertarDatos(connect,"credenciales",usr)
    return {"message":f"el usuario {user.username} ha sido registrado con exito"}