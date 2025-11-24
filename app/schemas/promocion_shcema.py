import uuid
from typing import Optional, TypeVar, Generic, List
from datetime import datetime
from decimal import Decimal
from pydantic import BaseModel, Field as PydanticField
from app.models.promocion_model import Promotion

class PromotionCreate(BaseModel):
    merchant_id: uuid.UUID
    title: str = PydanticField(..., max_length=255)
    description: Optional[str] = None
    discount_type: str = PydanticField(..., max_length=50)
    discount_value: Decimal = PydanticField(..., max_digits=10, decimal_places=2)
    start_date: datetime
    end_date: datetime
    is_active: bool = True

    class Config:
        orm_mode = True

class PromotionRead(BaseModel):
    id: uuid.UUID
    merchant_id: uuid.UUID
    title: str
    description: Optional[str]
    discount_type: str
    discount_value: Decimal
    start_date: datetime
    end_date: datetime
    is_active: bool

    class Config:
        orm_mode = True

T = TypeVar("T")
class Respons(BaseModel, Generic[T]):
    data: T

class PromotionResponse(Respons[Promotion]):
    pass

class PromotionReadResponse(Respons[PromotionRead]):
    pass

class PromotionListReadResponse(Respons[List[PromotionRead]]):
    pass
