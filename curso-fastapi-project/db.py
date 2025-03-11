from sqlmodel import SQLModel, create_engine,Session
from typing import Annotated
from fastapi import Depends, FastAPI

sqlite_name = "db.sqlite3" # Nombre de la base de datos
sqlite_url = f"sqlite:///{sqlite_name}" # URL de la base de datos
engine = create_engine(sqlite_url, echo=True) # Crea un motor de base de datos con la URL de la base de datos y activa el modo verbose para mostrar las consultas SQL que se ejecutan en la consola  

def create_all_tables(app:FastAPI): # Función para crear las tablas en la base de datos
    SQLModel.metadata.create_all(engine) # Crea las tablas en la base de datos
    yield

def get_session():# Función para obtener una sesión de base de datos
    with Session(engine) as session:# Crea una sesión de base de datos
        yield session # Retorna la sesión de base de datos

SessionDep = Annotated[Session, Depends(get_session)] # Anotación para inyectar una sesión de base de datos en un endpoint