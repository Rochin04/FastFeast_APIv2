import uuid
from typing import Optional, TypeVar, Generic, List
from pydantic import BaseModel
from app.models.estudiante_model import Estudiante

class EstudianteCreate(BaseModel):
    user_id: uuid.UUID
    student_id_number: str
    full_name: str
    profile_picture_url: Optional[str] = None
    # is_verified: bool = False
    
    class Config:
        orm_mode = True

class EstudianteUpdate(BaseModel):
    student_id_number: str
    full_name: str
    profile_picture_url: Optional[str] = None
    
    class Config:
        orm_mode = True

class EstudianteRead(BaseModel):
    # user_id: uuid.UUID
    student_id_number: str
    full_name: str
    profile_picture_url: Optional[str]
    is_verified: bool
    
    class Config:
        orm_mode = True

T = TypeVar("T")
class Respons(BaseModel, Generic[T]):
    data: T

class EstudianteResponse(Respons[Estudiante]):
    pass

class EstudianteReadResponse(Respons[EstudianteRead]):
    pass

class EstudianteListReadResponse(Respons[List[EstudianteRead]]):
    pass
