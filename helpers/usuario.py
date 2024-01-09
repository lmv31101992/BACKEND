from fastapi import HTTPException,status,Depends
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from helpers import basedatos,conexion
from jose import jwt, JWTError

ALGORITHM = "HS256"
ACCESS_TOKEN_DURATION = 5
SECRET = "201d573bd7d1344d3a3bfce1550b69102fd11be3db6d379508b6cccc58ea230b"
oauth2 = OAuth2PasswordBearer(tokenUrl="login")
crypt = CryptContext(schemes=["argon2"])

class User(BaseModel):
    username: str
    email: str
    full_name: str
    disabled: bool = False

class FullUser(User):
    password: str

def HashedPassword(password: str | None):
    # from argon2 import PasswordHasher
    from passlib.hash import argon2
    if password is None:
        return "no input password"
    return argon2.hash(password)


async def auth_user(token: str = Depends(oauth2)):
    exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Credenciales de autenticación inválidas",
        headers={"WWW-Authenticate": "Bearer"})
    try:
        pwd = jwt.decode(token, SECRET, algorithms=[ALGORITHM]).get("sub")
        if pwd is None:
            raise exception
    except JWTError:
        raise exception
    out = basedatos.recibirDatoPor("credenciales",conexion.abrirConexion(conexion.docker_list),"password",pwd)
    if out is not None:
        return User(**out)

async def current_user(user: User = Depends(auth_user)):
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="no hay datos de sesion de este usuario",
            headers={"WWW-Authenticate": "Bearer"})
    if user.disabled:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Usuario inactivo")
    return user