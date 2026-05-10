from datetime import datetime

from pydantic import EmailStr, Field

from app.models import CompanyRole
from app.schemas.common import ORMModel


class CompanyBase(ORMModel):
    name: str = Field(min_length=2, max_length=180)
    inn: str = Field(min_length=10, max_length=12)
    role: CompanyRole
    contact_name: str | None = None
    email: EmailStr | None = None
    phone: str | None = None
    address: str | None = None


class CompanyCreate(CompanyBase):
    pass


class CompanyRead(CompanyBase):
    id: int
    created_at: datetime

