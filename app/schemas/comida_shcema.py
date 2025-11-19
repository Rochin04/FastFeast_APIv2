import uuid
from decimal import Decimal
from pydantic import BaseModel
from typing import TypeVar, Generic, List
from app.models.comida_model import Comida
from pydantic import Field as PydanticField

class ComidaCreate(BaseModel):
    id: uuid.UUID
    name: str
    description: str
    price: Decimal = PydanticField(..., max_digits=10, decimal_places=2)
    category: str
    image_url: str
    merchant_id: uuid.UUID
    is_available: bool
    category_id: uuid.UUID
    class Config:
        orm_mode = True
class ComidaRead(BaseModel):
    id: uuid.UUID
    name: str
    description: str
    price: Decimal = PydanticField(..., max_digits=10, decimal_places=2)
    category: str
    image_url: str
    is_available: bool
    class Config:
        orm_mode = True 
T = TypeVar("T")
class Respons(BaseModel, Generic[T]):
    data: T

class ComidaResponse(Respons[Comida]):
    pass

class ComidaReadResponse(Respons[ComidaRead]):
    pass

class ComidaListReadResponse(Respons[List[ComidaRead]]):
    pass