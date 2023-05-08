from fastapi import APIRouter
from pydantic import BaseModel
from jwt_manager import create_token
from fastapi.responses import JSONResponse
from schemas.user import User

# Creamos el router para los usuarios
user_router = APIRouter()

# Movemos la class User(BAseModel) a schemas/user.py

# Creamos nueva ruta que permita al usuario loguearse
@user_router.post("/login", tags=["auth"])
def login(user: User):
    ## Validando token con el create_token que ya tenemos
    if user.email == "admin@gmail.com" and user.password == "adminpass":
        token: str = create_token(user.dict())
        return JSONResponse(status_code=200, content=token)
