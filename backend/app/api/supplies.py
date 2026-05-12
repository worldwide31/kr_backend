from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.auth import require_roles
from app.db.session import get_db
from app.schemas.supply import SupplyCreate, SupplyRead
from app.services.audit import write_event
from app.services.cache import invalidate
from app.services.serializers import supply_to_read
from app.services.supplies import create_supply as create_supply_service
from app.services.supplies import get_supply_or_404, list_supplies, receive_supply

router = APIRouter(prefix="/supplies", tags=["supplies"])


@router.get("", response_model=list[SupplyRead])
def read_supplies(
    db: Session = Depends(get_db),
    _: dict[str, str] = Depends(require_roles("admin", "operator")),
) -> list[dict]:
    return [supply_to_read(supply) for supply in list_supplies(db)]


@router.get("/{supply_id}", response_model=SupplyRead)
def read_supply(
    supply_id: int,
    db: Session = Depends(get_db),
    _: dict[str, str] = Depends(require_roles("admin", "operator")),
) -> dict:
    return supply_to_read(get_supply_or_404(db, supply_id))


@router.post("", response_model=SupplyRead, status_code=status.HTTP_201_CREATED)
async def create_supply(
    payload: SupplyCreate,
    db: Session = Depends(get_db),
    _: dict[str, str] = Depends(require_roles("admin", "operator")),
) -> dict:
    supply = create_supply_service(db, payload)
    db.commit()
    invalidate("dashboard:kpi")
    await write_event("create", "supply", supply.id, f"Создана поставка {supply.number}")
    return supply_to_read(supply)


@router.post("/{supply_id}/receive", response_model=SupplyRead)
async def receive(
    supply_id: int,
    db: Session = Depends(get_db),
    _: dict[str, str] = Depends(require_roles("admin", "operator")),
) -> dict:
    supply = receive_supply(db, supply_id)
    db.commit()
    invalidate("dashboard:kpi")
    await write_event("receive", "supply", supply.id, f"Поставка {supply.number} принята")
    return supply_to_read(supply)
