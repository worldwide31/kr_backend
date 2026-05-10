from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.dashboard import DashboardKpi
from app.services.dashboard import dashboard_kpi

router = APIRouter(prefix="/dashboard", tags=["dashboard"])


@router.get("/kpi", response_model=DashboardKpi)
def get_kpi(db: Session = Depends(get_db)) -> dict:
    return dashboard_kpi(db)

