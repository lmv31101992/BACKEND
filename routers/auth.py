from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import  OAuth2PasswordRequestForm
from jose import jwt, JWTError
from helpers import basedatos,usuario,conexion

router = APIRouter()
connect = conexion.abrirConexion(conexion.docker_list)

@router.post("/login")
async def login(form: OAuth2PasswordRequestForm = Depends()):
    if not connect:   
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Fallo en conexion con la BBDD",
            headers={"WWWW-Autenticate":"Bearer"})    #aqui deber coge los datos del usuario que llega en el cuerpo del formulario
    conexion.crearTabla(connect,"credenciales")

    user = basedatos.recibirDatoPor("credenciales",connect,"username",form.username)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="El usuario no es correcto")
    user = usuario.FullUser(**user)

    #se verifica si la contraseña hasheada es igual al de la bbdd
    if not usuario.crypt.verify(form.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="La contraseña no es correcta")
    access_token = {"sub": user.password}
    return {"access_token": jwt.encode(access_token, usuario.SECRET, algorithm=usuario.ALGORITHM), "token_type": "bearer"}

@router.get("/list")
async def me(user: usuario.User = Depends(usuario.current_user)):
    if user is None:
        return {"message":"credencial de token invalida"}    
    return basedatos.recibirDatos(connect,"credenciales")