from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


class ORMModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class MoneyMixin(BaseModel):
    total: Decimal = Field(default=Decimal("0.00"))

