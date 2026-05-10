from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models import Company
from app.schemas.company import CompanyCreate, CompanyRead
from app.services.audit import write_event
from app.services.cache import invalidate

router = APIRouter(prefix="/companies", tags=["companies"])


@router.get("", response_model=list[CompanyRead])
def list_companies(db: Session = Depends(get_db)) -> list[Company]:
    return list(db.scalars(select(Company).order_by(Company.name)))


@router.post("", response_model=CompanyRead, status_code=status.HTTP_201_CREATED)
async def create_company(payload: CompanyCreate, db: Session = Depends(get_db)) -> Company:
    duplicate = db.scalar(select(Company).where((Company.inn == payload.inn) | (Company.name == payload.name)))
    if duplicate:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Контрагент с таким названием или ИНН уже есть. Проверьте справочник перед созданием.",
        )
    company = Company(**payload.model_dump())
    db.add(company)
    db.commit()
    db.refresh(company)
    invalidate("dashboard:kpi")
    await write_event("create", "company", company.id, f"Создан контрагент {company.name}")
    return company
