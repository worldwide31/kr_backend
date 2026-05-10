from decimal import Decimal

from pydantic import Field

from app.schemas.common import ORMModel


class ProductBase(ORMModel):
    sku: str = Field(min_length=2, max_length=64)
    name: str = Field(min_length=2, max_length=180)
    category: str = Field(min_length=2, max_length=120)
    unit: str = "шт"
    purchase_price: Decimal = Field(ge=0)
    sale_price: Decimal = Field(ge=0)
    min_stock: int = Field(default=0, ge=0)


class ProductCreate(ProductBase):
    pass


class ProductRead(ProductBase):
    id: int

