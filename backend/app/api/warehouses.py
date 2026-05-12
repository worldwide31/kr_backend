from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.core.auth import require_roles
from app.db.session import get_db
from app.models import InventoryItem, Warehouse
from app.schemas.warehouse import InventoryRead, WarehouseCreate, WarehouseRead
from app.services.audit import write_event
from app.services.cache import invalidate
from app.services.serializers import inventory_to_read

router = APIRouter(prefix="/warehouses", tags=["warehouses"])


@router.get("", response_model=list[WarehouseRead])
def list_warehouses(
    db: Session = Depends(get_db),
    _: dict[str, str] = Depends(require_roles("admin", "operator")),
) -> list[Warehouse]:
    return list(db.scalars(select(Warehouse).order_by(Warehouse.city, Warehouse.name)))


@router.post("", response_model=WarehouseRead, status_code=status.HTTP_201_CREATED)
async def create_warehouse(
    payload: WarehouseCreate,
    db: Session = Depends(get_db),
    _: dict[str, str] = Depends(require_roles("admin")),
) -> Warehouse:
    duplicate = db.scalar(select(Warehouse).where(Warehouse.name == payload.name))
    if duplicate:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Склад с таким названием уже создан. Используйте другое название или выберите существующий склад.",
        )
    warehouse = Warehouse(**payload.model_dump())
    db.add(warehouse)
    db.commit()
    db.refresh(warehouse)
    invalidate("dashboard:kpi")
    await write_event("create", "warehouse", warehouse.id, f"Создан склад {warehouse.name}")
    return warehouse


@router.get("/inventory", response_model=list[InventoryRead])
def list_inventory(
    db: Session = Depends(get_db),
    _: dict[str, str] = Depends(require_roles("admin", "operator")),
) -> list[dict]:
    items = db.scalars(
        select(InventoryItem)
        .options(selectinload(InventoryItem.product), selectinload(InventoryItem.warehouse))
        .order_by(InventoryItem.warehouse_id, InventoryItem.product_id)
    )
    return [inventory_to_read(item) for item in items]
