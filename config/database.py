# Añadir configuraciones
import os
from sqlalchemy import create_engine
from sqlalchemy.orm.session import sessionmaker
from sqlalchemy.ext.declarative import declarative_base # PAra manipular las tablas de la base de datos

sqlite_file_name = "../database.sqlite"

# Leer el directorio actual del archivo 
base_dir = os.path.dirname(os.path.realpath(__file__))

# Crear URL de la base de datos
database_url = f"sqlite:///{os.path.join(base_dir, sqlite_file_name)}"

# Motor de la base de datos.
## Parámetro echo para que muetre por consola lo que se está realizando, es decir el código
engine = create_engine(database_url, echo=True)

# Crear sesión para conectarnos a la base de datos
Session = sessionmaker(bind=engine)

# Manejo de las tablas de base de datos
Base = declarative_base()