import uuid
from decimal import Decimal
from datetime import time
from typing import Optional 
from sqlmodel import Field, SQLModel
from sqlalchemy import Column, func
from sqlalchemy.types import UUID, Numeric 

class Merchant(SQLModel, table=True):
    __tablename__ = "merchants"
    id: Optional[uuid.UUID] = Field(
    default=None,
    sa_column=Column(
        UUID(as_uuid=True),
        server_default=func.gen_random_uuid(),
        primary_key=True
    )
)
    owner_id: uuid.UUID = Field(foreign_key="users.id")
    name: str = Field(max_length=255)
    location_latitude: Decimal = Field(sa_column=Column(Numeric(10, 8)))
    location_longitude: Decimal = Field(sa_column=Column(Numeric(11, 8)))
    is_validated: bool = Field(default=False, nullable=False)
    description: Optional[str] = Field(default=None)
    logo_url: Optional[str] = Field(default=None, max_length=255)
    address: Optional[str] = Field(default=None, max_length=255)
    opening_time: Optional[time] = Field(default=None)
    closing_time: Optional[time] = Field(default=None)
