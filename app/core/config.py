import os
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # Definimos la variable, pero NO le damos valor aquí.
    # Pydantic buscará una variable llamada "DATABASE_URL" en el sistema.
    DATABASE_URL: str

    CONNECT_ARGS: dict = {} 

    # Configuración para que lea el archivo .env localmente
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore" # Ignora otras variables del .env si las hubiera
    )

settings = Settings()