from pydantic import BaseModel, Field

# Creamos un nuevo modelo para el usuario
class User(BaseModel):
    email: str
    password: str