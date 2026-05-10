from pydantic import Field

from app.schemas.common import ORMModel


class WarehouseBase(ORMModel):
    name: str = Field(min_length=2, max_length=160)
    city: str = Field(min_length=2, max_length=100)
    address: str = Field(min_length=5)
    manager: str | None = None


class WarehouseCreate(WarehouseBase):
    pass


class WarehouseRead(WarehouseBase):
    id: int


class InventoryRead(ORMModel):
    id: int
    product_id: int
    warehouse_id: int
    product_name: str
    sku: str
    warehouse_name: str
    quantity: int
    reserved: int
    available: int
    min_stock: int

