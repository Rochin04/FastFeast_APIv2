import uuid
from typing import Optional
from sqlalchemy import Column, func
from sqlalchemy.types import UUID
from sqlmodel import Field, SQLModel

class Category(SQLModel, table=True):
    __tablename__ = "categories"
    id: Optional[uuid.UUID] = Field(
        default=None,
        sa_column=Column(
            UUID(as_uuid=True), 
            server_default=func.gen_random_uuid(), 
            primary_key=True
        )
    )
    name: str = Field(max_length=100, unique=True)