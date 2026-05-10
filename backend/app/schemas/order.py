from datetime import datetime
from decimal import Decimal

from pydantic import Field

from app.models import OrderStatus
from app.schemas.common import ORMModel


class OrderItemCreate(ORMModel):
    product_id: int
    warehouse_id: int
    quantity: int = Field(gt=0)
    unit_price: Decimal = Field(ge=0)


class OrderCreate(ORMModel):
    customer_id: int
    delivery_city: str = Field(min_length=2, max_length=100)
    comment: str | None = None
    items: list[OrderItemCreate] = Field(min_length=1)


class OrderItemRead(ORMModel):
    id: int
    product_id: int
    warehouse_id: int
    product_name: str
    warehouse_name: str
    quantity: int
    unit_price: Decimal
    total: Decimal


class OrderRead(ORMModel):
    id: int
    number: str
    customer_id: int
    customer_name: str
    status: OrderStatus
    delivery_city: str
    comment: str | None
    created_at: datetime
    total: Decimal
    items: list[OrderItemRead]

