from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.services.cache import invalidate
from app.utils.seed import seed_demo_data

router = APIRouter(prefix="/seed", tags=["system"])


@router.post("")
def seed(db: Session = Depends(get_db)) -> dict[str, str]:
    seed_demo_data(db)
    invalidate("dashboard:kpi")
    return {"status": "demo data ready"}
