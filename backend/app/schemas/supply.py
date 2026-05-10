from datetime import datetime
from decimal import Decimal

from pydantic import Field

from app.models import SupplyStatus
from app.schemas.common import ORMModel


class SupplyItemCreate(ORMModel):
    product_id: int
    warehouse_id: int
    quantity: int = Field(gt=0)
    purchase_price: Decimal = Field(ge=0)


class SupplyCreate(ORMModel):
    supplier_id: int
    eta: datetime | None = None
    items: list[SupplyItemCreate] = Field(min_length=1)


class SupplyItemRead(ORMModel):
    id: int
    product_id: int
    warehouse_id: int
    product_name: str
    warehouse_name: str
    quantity: int
    purchase_price: Decimal
    total: Decimal


class SupplyRead(ORMModel):
    id: int
    number: str
    supplier_id: int
    supplier_name: str
    status: SupplyStatus
    eta: datetime | None
    created_at: datetime
    total: Decimal
    items: list[SupplyItemRead]

