from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.auth import require_roles
from app.db.session import get_db
from app.schemas.dashboard import DashboardKpi
from app.services.dashboard import dashboard_kpi

router = APIRouter(prefix="/dashboard", tags=["dashboard"])


@router.get("/kpi", response_model=DashboardKpi)
def get_kpi(
    db: Session = Depends(get_db),
    _: dict[str, str] = Depends(require_roles("admin", "operator")),
) -> dict:
    return dashboard_kpi(db)
