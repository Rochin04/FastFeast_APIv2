import uuid
from decimal import Decimal
from datetime import datetime
from typing import Optional
from sqlmodel import Field, SQLModel
from sqlalchemy import Column, func
from sqlalchemy.types import UUID, Numeric, DateTime

class Promotion(SQLModel, table=True):
    __tablename__ = "promotions"

    id: Optional[uuid.UUID] = Field(
        default=None,
        sa_column=Column(
            UUID(as_uuid=True),
            server_default=func.gen_random_uuid(),
            primary_key=True
        )
    )
    merchant_id: uuid.UUID = Field(foreign_key="merchants.id", nullable=False)
    title: str = Field(max_length=255, nullable=False)
    description: Optional[str] = Field(default=None)
    discount_type: str = Field(max_length=50, nullable=False)
    discount_value: Decimal = Field(sa_column=Column(Numeric(10, 2), nullable=False))
    start_date: datetime = Field(sa_column=Column(DateTime(timezone=True), nullable=False))
    end_date: datetime = Field(sa_column=Column(DateTime(timezone=True), nullable=False))
    is_active: bool = Field(default=True, nullable=False)
#(discount_type::text = ANY (ARRAY['percentage'::character varying, 'fixed_amount'::character 
# varying, '2x1'::character varying, 'combo'::character varying]::text[]))