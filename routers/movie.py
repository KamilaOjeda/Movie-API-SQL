from fastapi import APIRouter
from fastapi import Path, Query, Depends
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import List, Optional
# Importamos el archivo de la base de datos
from config.database import Session
from models.movie import Movie as MovieModel # Para que sea un nombre distinto al que ya tenemos en este archivo
from fastapi.encoders import jsonable_encoder
from middlewares.jwt_bearer import JWTBearer
from services.movie import MovieService
from schemas.movie import Movie

# Creamos el router
movie_router = APIRouter()

# Movimos la class Movie(BaseModel) a schemas   

@movie_router.get("/movies", tags=["movies"], 
         response_model=List[Movie], 
         status_code=200, dependencies=[Depends(JWTBearer())])
def get_movies() -> List[Movie]:
    ## Crear una instancia de la session
    db = Session()
    result = MovieService(db).get_movies()
    # ## Consultar los datos
    # result = db.query(MovieModel).all()
    return JSONResponse(status_code=200, content = jsonable_encoder(result))
    # return JSONResponse(status_code=200, content = movies)

# Parámetros de ruta
@movie_router.get("/movies/{id}", tags=["movies"], response_model=Movie)
def get_movie(id: int = Path(ge=1, le=2000)) -> Movie: ## Agregamos validaciones de parámetros de ruta con Path
    ## Crear la instancia de la session
    db = Session()
    result = MovieService(db).get_movie(id)
    if not result:
        return JSONResponse(status_code=404, content={"message": "No encontrado"})
    return JSONResponse(status_code=200, content=jsonable_encoder(result))
    # for item in movies:
    #     if item["id"] == id:
    #         return JSONResponse(content = item)
    # return JSONResponse(status_code=404, content={"message": "No se ha encontrado la página"})

# Parámetros query, cuando no se indica en la ruta, si no como parámetro
# @movie_router.get("/movies/", tags=["movies"])
# def get_movies_by_category(category: str, year: int):
#     return category, year

# Parámetros query, filtrando por categoría
@movie_router.get("/movies/", tags=["movies"], response_model=List[Movie], status_code=200)
def get_movies_by_category(category: str = Query(min_length=5, max_length=15)) -> List[Movie]: ## Agregamos validación de parámetros query
    ## Crear instancia de la session
    db = Session()
    result = MovieService(db).get_movie_by_category(category)
    if not result:
        return JSONResponse(status_code=404, content={"message": "No encontrado"})
    return JSONResponse(status_code=200, content=jsonable_encoder(result))

    # data = [ item for item in movies if item["category"] == category]
    # return JSONResponse(content=data)

# Método POST
@movie_router.post("/movies", tags=["movies"], response_model=dict, status_code=201)
# def create_movie(id: int = Body(), tittle: str = Body(), overview: str = Body(), year: int = Body(), rating: float = Body(), category: str = Body()):
def create_movie(movie: Movie) -> dict: ## En vez de poner cada elemento del body, utilizamos este atajo
    ## Crear una sesión para conectarnos a la Base de Datos
    db = Session()
    MovieService(db).create_movie(movie)
    # new_movie = MovieModel(**movie.dict()) ## Conviernte movie en un diccionario y con ** pasamos todos los parámetros de movie.
    # db.add(new_movie) ## Añadimos la película que se acaba de crear.
    # db.commit() ## Actualización para que los datos se guarden
    # movies.movie_routerend(movie) # Insertar datos
    return JSONResponse(status_code=201, content={"message": "Se ha registrado la película"}) # devolvemos un diccionario

# # Método PUT, como parámetro de ruta
# @movie_router.put("/movies/{id}", tags=["movies"])
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
@movie_router.put("/movies/{id}", tags=["movies"], response_model=dict, status_code=200)
def update_movie(id: int, movie: Movie) -> dict:
    ## Creando session
    db = Session()
    result = MovieService(db).get_movie(id)
    if not result:
        return JSONResponse(status_code=404, content={"message": "No encontrado"})
    
    MovieService(db).update_movie(id, movie)
    return JSONResponse(status_code=200, content={"message": "Se ha modificado la película"}) # devolvemos un diccionario

    # for item in movies:
    #     if item["id"] == id:
    #         item["tittle"] = movie.tittle
    #         item["overview"] = movie.overview
    #         item["year"] = movie.year
    #         item["rating"] = movie.rating
    #         item["category"] = movie.category
    #         return JSONResponse(status_code=200, content={"message": "Se ha modificado la película"}) # devolvemos un diccionario

# Método DELETE, como parámetro de ruta
@movie_router.delete("/movies/{id}", tags=["movies"], response_model=dict, status_code=200)
def delete_movie(id: int) -> dict:
    # Crear session
    db = Session()
    result: MovieModel = db.query(MovieModel).filter(MovieModel.id == id).first()
    if not result:
        return JSONResponse(status_code=404, content={"message": "No encontrado"})
    MovieService(db).delete_movie(id)
    return JSONResponse(status_code=200, content={"message": "Se ha eliminado la película"}) # devolvemos un diccionario

    # for item in movies:
    #     if item["id"] == id:
    #         movies.remove(item)
    #         return JSONResponse(status_code=200, content={"message": "Se ha eliminado la película"}) # devolvemos un diccionario

 