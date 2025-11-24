import uuid
from pydantic import BaseModel, Field as PydanticField
from typing import TypeVar, Generic, List
from app.models.usuarios_model import Usuario

class UsuarioCreate(BaseModel):
    email: str = PydanticField(..., max_length=255, unique=True)
    password_hash: str = PydanticField(..., max_length=255)
    user_type: str = PydanticField(..., max_length=50)
    class Config:
        orm_mode = True

class UsuarioRead(BaseModel):
    id: uuid.UUID
    email: str
    user_type: str
    class Config:
        orm_mode = True

class UsuarioUpdate(BaseModel):
    email: str = PydanticField(..., max_length=255, unique=True)
    password_hash: str = PydanticField(..., max_length=255)
    class Config:
        orm_mode = True

T = TypeVar("T")
class Respons(BaseModel, Generic[T]):
    data: T

class UsuarioResponse(Respons[Usuario]):
    pass

class UsuarioReadResponse(Respons[UsuarioRead]):
    pass

class UsuarioListReadResponse(Respons[List[UsuarioRead]]):
    pass