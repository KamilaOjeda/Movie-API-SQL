from fastapi import APIRouter
from pydantic import BaseModel
from jwt_manager import create_token
from fastapi.responses import JSONResponse

# Creamos el router para los usuarios
user_router = APIRouter()

# Creamos un nuevo modelo para el usuario
class User(BaseModel):
    email: str
    password: str

# Creamos nueva ruta que permita al usuario loguearse
@user_router.post("/login", tags=["auth"])
def login(user: User):
    ## Validando token con el create_token que ya tenemos
    if user.email == "admin@gmail.com" and user.password == "adminpass":
        token: str = create_token(user.dict())
        return JSONResponse(status_code=200, content=token)
