# Creación de modelos
## Creación de modelos de la tabla de movies
from config.database import Base
from sqlalchemy import Column, Integer, String, Float

# Movie hereda de Base, es una entidad de la BD
# Tabla películas
class Movie(Base):
    
    __tablename__ = "movies"
    
    id = Column(Integer, primary_key = True)
    tittle = Column(String)
    overview = Column(String)
    year = Column(Integer)
    rating = Column(Float)
    category = Column(String)



