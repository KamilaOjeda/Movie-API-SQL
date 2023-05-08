# Servicios para consultar datos
from models.movie import Movie as MovieModel
from schemas.movie import Movie

# Clase.Servicio para tener las películas
class MovieService():
    # Método constructor: Cada vez que se llame a este servicio, se envia a la base de datos.
    def __init__(self, db) -> None: #Recuerda que son dos guines bajos, _ _
        self.db = db
        
    # Creamos el 1er método de la clase, por eso tienen el atributo self
    def get_movies(self):
        # Ejecutar el query
        result = self.db.query(MovieModel).all()
        return result
    
     # Para movie por id
    def get_movie(self, id):
        # Ejecutar el query
        result = self.db.query(MovieModel).filter(MovieModel.id == id).first()
        return result
    
     # Para movie por categoría
    def get_movie_by_category(self, category):
        # Ejecutar el query
        result = self.db.query(MovieModel).filter(MovieModel.category == category).all()
        return result

    # Método, desde la entidad de los base de datos enviar las propiedades
    def create_movie(self, movie: Movie):
        new_movie = MovieModel(**movie.dict())
        self.db.add(new_movie)
        self.db.commit()
        return
    
    # Método para modificar datos
    def update_movie(self, id: int, data: Movie):
        movie = self.db.query(MovieModel).filter(MovieModel.id == id).first()
        movie.tittle = data.tittle
        movie.overview = data.overview
        movie.year = data.year
        movie.rating = data.rating
        movie.category = data.category
        self.db.commit()
        return
    
     # Método, para eliminar
    def delete_movie(self, id: int):
        self.db.query(MovieModel).filter(MovieModel.id == id).delete()
        self.db.commit()
        return

        
# Todo esto lo importamos en el router de movies