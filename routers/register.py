from fastapi import APIRouter, FastAPI,status,HTTPException,Depends
from fastapi.security import OAuth2AuthorizationCodeBearer,OAuth2PasswordRequestForm
from clases import Conexion,BaseDatos,Usuario
# from test_main import get_bbdd_instance,get_conexion_instance,get_usuario_instance

router = APIRouter()
# access_list_bbdd = ['bd_pruebas',"postgres",'admin',"127.0.0.1","5432"]

# conexion = Conexion(access_list_bbdd)
# bbdd = BaseDatos()
# u = Usuario()

@router.post("/register")
# async def recurso(user:OAuth2PasswordRequestForm=Depends()):


# async def login(
#     user: OAuth2PasswordRequestForm = Depends(),
#     conexion: Conexion = Depends(get_conexion_instance),
#     bbdd: BaseDatos = Depends(get_bbdd_instance),
#     u: Usuario = Depends(get_usuario_instance)):
async def login(
    user: OAuth2PasswordRequestForm = Depends(),
    conexion: Conexion = Depends(),
    bbdd: BaseDatos = Depends(),
    u: Usuario = Depends(),
):
    # global conexion
    # global bbdd
    #comprueba si la conexion es correcta
    if not conexion.abrirConexion():
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Fallo en conexion con base de datos", 
            headers={"WWWW-Autenticate":"Bearer"})
    # se llama a la funcion createTable para crear la tabla de credenciales en la base de datos por sino existiera
    conexion.crearTabla("credenciales")
    #comprueba si ya existe el usuario
    if bbdd.existeUsername("credenciales",conexion.abrirCursor(),user.username):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="USUARIO REGISTRADO!", 
            headers={"WWWW-Autenticate":"Bearer"})
    
    #tenemos que codificar ese pwd y agregarlo a la bbdd
    usr = [user.username,user.username,"",u.HashedPassword_New(user.password),False]
    bbdd.insertarDatos(conexion.abrirCursor(),usr)
    # setUser(conexion,user.username,user.username,"",HashedPassword(user.password),False)
    return {"message":f"el usuario {user.username} ha sido registrado con exito"}