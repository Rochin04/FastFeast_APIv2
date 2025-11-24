import uuid
from typing import Optional, TypeVar, Generic, List
from datetime import time
from decimal import Decimal
from pydantic import BaseModel, Field as PydanticField
from app.models.comerciante_model import Merchant

class MerchantCreate(BaseModel):
    owner_id: uuid.UUID
    name: str
    description: Optional[str] = None
    logo_url: Optional[str] = None
    location_latitude: Decimal = PydanticField(..., max_digits=10, decimal_places=8)
    location_longitude: Decimal = PydanticField(..., max_digits=11, decimal_places=8)
    address: Optional[str] = None
    opening_time: Optional[time] = None
    closing_time: Optional[time] = None
    # is_validated: bool = False

    class Config:
        orm_mode = True

class MerchantRead(BaseModel):
    id: uuid.UUID
    owner_id: uuid.UUID
    name: str
    description: Optional[str]
    logo_url: Optional[str]
    location_latitude: Decimal
    location_longitude: Decimal
    address: Optional[str]
    opening_time: Optional[time]
    closing_time: Optional[time]
    is_validated: bool

    class Config:
        orm_mode = True

T = TypeVar("T")
class Respons(BaseModel, Generic[T]):
    data: T

class MerchantResponse(Respons[Merchant]):
    pass

class MerchantReadResponse(Respons[MerchantRead]):
    pass

class MerchantListReadResponse(Respons[List[MerchantRead]]):
    pass
