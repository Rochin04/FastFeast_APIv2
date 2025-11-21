import uuid
from typing import Optional
from sqlalchemy import Column, ForeignKey
from sqlalchemy.types import UUID
from sqlmodel import Field, SQLModel

class Estudiante(SQLModel, table=True):
    __tablename__ = "students"
    user_id: uuid.UUID = Field(
        sa_column=Column(
            UUID(as_uuid=True),
            ForeignKey("users.id", ondelete="CASCADE"),
            primary_key=True
        )
    )
    student_id_number: str = Field(max_length=100, unique=True)
    full_name: str = Field(max_length=255)
    profile_picture_url: Optional[str] = Field(default=None, max_length=255)
    is_verified: bool = Field(default=False)
