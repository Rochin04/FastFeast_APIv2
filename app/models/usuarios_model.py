import uuid
from typing import Optional
from sqlalchemy import Column, func
from sqlalchemy.types import UUID
from sqlmodel import Field, SQLModel

class Usuario(SQLModel, table=True):
    __tablename__ = "users"
    id: Optional[uuid.UUID] = Field(
        default=None,
        sa_column=Column(
            UUID(as_uuid=True), 
            server_default=func.gen_random_uuid(), 
            primary_key=True
        )
    )
    email: str = Field(max_length=255, unique=True)
    password_hash: str = Field(max_length=255)
    user_type: str = Field(max_length=50)#student, merchant