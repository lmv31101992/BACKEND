from fastapi import APIRouter, Depends, HTTPException, status
from helpers import basedatos,usuario,conexion
from fastapi import HTTPException,status,Depends

router = APIRouter()
connect = conexion.abrirConexion(conexion.docker_list)


@router.delete("/")
async def BorrarUsuario(username:str , user: usuario.User = Depends(usuario.current_user)):
    if not connect:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Fallo en conexion con base de datos", 
            headers={"WWWW-Autenticate":"Bearer"})
    if user is None:
        return {"message":"credencial de token invalida"}
    if not basedatos.existeUsername(connect,"credenciales",username):
        return {"message": f"no se puede eliminar el usuario {username}",}
    basedatos.eliminarDatos(connect,"credenciales",username)
    return {"message": f"se elimina el usuario {username}",}