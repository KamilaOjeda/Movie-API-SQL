from jwt import encode, decode

# Crear función para crear el token
## Le pasamos un diccionario como parámetro
## payload: el contenido que se pasa como token
def create_token(data: dict) -> str:
   token: str = encode(payload=data, key="my_secrete_key", algorithm="HS256")
   return token

# Crear función para validar el token/ importamos decode
def validate_token(token: str) -> dict:
   data: dict = decode(token, key="my_secrete_key", algorithms=["HS256"])
   return data