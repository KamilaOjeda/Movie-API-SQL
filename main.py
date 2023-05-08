from fastapi import FastAPI, Body, Path, Query, Request, Depends, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel, Field
from typing import Optional, List
from jwt_manager import create_token, validate_token
from fastapi.security import HTTPBearer

app = FastAPI()
app.title = "Mi primera app con FastAPI"
app.version = "0.0.1"

# Creamos una nueva clase que herda la clase HTTPBearear
## funcion call: recibe petición y devuelve la credenciales del usuario
class JWTBearer(HTTPBearer):
    async def __call__(self, request: Request):
        auth = await super().__call__(request)
        data = validate_token(auth.credentials)
        if data["email"] != "admin@gmail.com":
            raise HTTPException(status_code=403, detail="Credenciales inválidas")

# Creamos un nuevo modelo para el usuario
class User(BaseModel):
    email: str
    password: str

# Creamos la clase/esquema que va a contener tod la info de cada película
class Movie(BaseModel):
    # id: int | None = None ## None es para indicar que puede ser opcional, sin embargo hay otra forma: tiping.
    id: Optional[int] = None
    ## Se pueden agregar validaciones importando Field
    tittle: str = Field(min_length=5, max_length=15)
    overview: str = Field(min_length=15, max_length=50)
    year: int = Field(le=2022)
    rating: float = Field(..., ge=1, le=10) ## el menor es 1, ge= greater tahn o equal to, y el max es 10, le=less than or equal to. Los puntos suspensivos indican que el campo es obligatorio y no puede ser nulo
    category: str

    ## Agregamos una clase de ejemplo de como deberia estar formado el objeto de cada película.
    class Config:
        schema_extra = {
            "example": {
                "id": 1,
                "tittle": "Mi película",
                "overview": "Sinopsis de la película",
                "year": 2022,
                "rating": 7.8,
                "category": "Drama"
            }
        }
        
movies = [
    {
        "id": 1,
    "tittle": "Avatar",
    "overview": "En un exhuberante planeta llamado Pandora, viven los Na'vi",
    "year": "2009",
    "rating": "7.8",
    "category": "Acción"
    },
    {
        "id": 2,
    "tittle": "Avatar",
    "overview": "En un exhuberante planeta llamado Pandora, viven los Na'vi",
    "year": "2009",
    "rating": "7.8",
    "category": "Acción"
    }
]

# Método GET
@app.get("/", tags=["home"])
def message():
    return HTMLResponse("<h1>Hello world<h1>")

# Creamos nueva ruta que permita al usuario loguearse
@app.post("/login", tags=["auth"])
def login(user: User):
    ## Validando token con el create_token que ya tenemos
    if user.email == "admin@gmail.com" and user.password == "adminpass":
        token: str = create_token(user.dict())
        return JSONResponse(status_code=200, content=token)

@app.get("/movies", tags=["movies"], 
         response_model=List[Movie], 
         status_code=200, 
         dependencies=[Depends(JWTBearer())])
def get_movies() -> List[Movie]:
    return JSONResponse(status_code=200, content = movies)

# Parámetros de ruta
@app.get("/movies/{id}", tags=["movies"], response_model=Movie)
def get_movie(id: int = Path(ge=1, le=2000)) -> Movie: ## Agregamos validaciones de parámetros de ruta con Path
    for item in movies:
        if item["id"] == id:
            return JSONResponse(content = item)
    return JSONResponse(status_code=404, content={"message": "No se ha encontrado la página"})

# Parámetros query, cuando no se indica en la ruta, si no como parámetro
# @app.get("/movies/", tags=["movies"])
# def get_movies_by_category(category: str, year: int):
#     return category, year

# Parámetros query, filtrando por categoría
@app.get("/movies/", tags=["movies"], response_model=List[Movie], status_code=200)
def get_movies_by_category(category: str = Query(min_length=5, max_length=15)) -> List[Movie]: ## Agregamos validación de parámetros query
    data = [ item for item in movies if item["category"] == category]
    return JSONResponse(content=data)

# Método POST
@app.post("/movies", tags=["movies"], response_model=dict, status_code=201)
# def create_movie(id: int = Body(), tittle: str = Body(), overview: str = Body(), year: int = Body(), rating: float = Body(), category: str = Body()):
def create_movie(movie: Movie) -> dict: ## En vez de poner cada elemento del body, utilizamos este atajo
    movies.append(movie) # Insertar datos
    return JSONResponse(status_code=201, content={"message": "Se ha registrado la película"}) # devolvemos un diccionario

# # Método PUT, como parámetro de ruta
# @app.put("/movies/{id}", tags=["movies"])
# def update_movie(id: int, tittle: str = Body(), overview: str = Body(), year: int = Body(), rating: float = Body(), category: str = Body()):
#     for item in movies:
#         if item["id"] == id:
#             item["tittle"] = tittle,
#             item["overview"] = overview,
#             item["year"] = year,
#             item["rating"] = rating, 
#             item["category"] = category
#             return movies

# Método PUT, como parámetro de ruta
@app.put("/movies/{id}", tags=["movies"], response_model=dict, status_code=200)
def update_movie(id: int, movie: Movie) -> dict:
    for item in movies:
        if item["id"] == id:
            item["tittle"] = movie.tittle
            item["overview"] = movie.overview
            item["year"] = movie.year
            item["rating"] = movie.rating
            item["category"] = movie.category
            return JSONResponse(status_code=200, content={"message": "Se ha modificado la película"}) # devolvemos un diccionario

# Método DELETE, como parámetro de ruta
@app.delete("/movies/{id}", tags=["movies"], response_model=dict, status_code=200)
def update_movie(id: int) -> dict:
    for item in movies:
        if item["id"] == id:
            movies.remove(item)
            return JSONResponse(status_code=200, content={"message": "Se ha eliminado la película"}) # devolvemos un diccionario

        
# Validaciones de tipos de datos
## importamos field desde pydantic
## indicar en el esquema con la palabra Field

# Validaciones de parámetros de ruta y query
## importamos path desde fastapi
## importamos query desde fastapi

# Tipos de respuestas
## importamos JSONResponse desde fastapi.responses, sirve para enviar contenido en formato JSON al cliente
## importamos List desde typing, sirve para indicar el modelo de respuesta

#Códigos de estado
## status_code

# Función para generar tokens con pyjwt
## pip3 install pyjwt
## creamos archivo jwt_manager.py
## ahora importamos create_token(que está en el el archivo jwt_manager.py)

# Validando tokens
## vamos a la instancia del usuario
## en jwt_manager.py importamos decode.

# Middlewares de autenticación
## importamos validate_token, request
## importamos from fastapi.security import HTTPBearer
## importamos Depends, se le pasa la clase de la cual depende