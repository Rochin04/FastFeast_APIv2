import uuid
from decimal import Decimal
from typing import Optional
from sqlalchemy import Column, func
from sqlalchemy.types import UUID, Numeric
from sqlmodel import Field, SQLModel
from .comerciante_model import Merchant

class Comida(SQLModel, table=True):
    __tablename__ = "dishes"
    id: Optional[uuid.UUID] = Field(
        default=None,
        sa_column=Column(
            UUID(as_uuid=True), 
            server_default=func.gen_random_uuid(), 
            primary_key=True
        )
    )
    merchant_id: uuid.UUID = Field(foreign_key="merchants.id")
    category_id: uuid.UUID = Field(foreign_key="categories.id")
    name: str = Field(max_length=255)
    description: Optional[str] = Field(default=None)
    price: Decimal = Field(sa_column=Column(Numeric(10, 2)))
    image_url: Optional[str] = Field(default=None, max_length=255)
    category: Optional[str] = Field(default=None, max_length=100)
    is_available: bool = Field(default=True)