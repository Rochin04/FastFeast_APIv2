import uuid
from sqlmodel import Field, SQLModel
from sqlalchemy import Column
from sqlalchemy.types import UUID, Numeric
from sqlmodel import Field, SQLModel
from sqlalchemy.types import UUID, Numeric

class Categoria(SQLModel, table=True):
    __tablename__ = "categories"
    id: Optional[uuid.UUID] = Field(
        default=None,
        sa_column=Column(
            UUID(as_uuid=True), 
            server_default=func.gen_random_uuid(), 
            primary_key=True
        )
    )
    name: str = Field(max_length=255)