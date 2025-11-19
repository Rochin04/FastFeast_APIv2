import uuid
from pydantic import BaseModel, Field as PydanticField
from typing import TypeVar, Generic, List
from app.models.category_model import Category

class CategoryCreate(BaseModel):
    name: str = PydanticField(..., max_length=100)

    class Config:
        orm_mode = True

class CategoryRead(BaseModel):
    id: uuid.UUID
    name: str = PydanticField(..., max_length=100)

    class Config:
        orm_mode = True

T = TypeVar("T")
class Respons(BaseModel, Generic[T]):
    data: T

class CategoryResponse(Respons[Category]):
    pass

class CategoryReadResponse(Respons[CategoryRead]):
    pass

class CategoryListReadResponse(Respons[List[CategoryRead]]):
    pass