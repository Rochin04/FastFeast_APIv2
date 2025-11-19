import os
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DB_USER: str = "postgres"  # Usuario por defecto de postgres
    DB_PASSWORD: str = "emirochi_0122X"  # La contraseña que estableciste para tu usuario
    DB_HOST: str = "localhost"
    DB_PORT: str = "5432"      # Puerto por defecto de postgres
    DB_NAME: str = "fastfeastdb"  # El nombre de la base de datos a la que te quieres conectar
    DATABASE_URL: str = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    CONNECT_ARGS: dict = {}
    class Config:
        case_sensitive = True
settings = Settings()

