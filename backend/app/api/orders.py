from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.auth import require_roles
from app.db.session import get_db
from app.schemas.order import OrderCreate, OrderRead
from app.services.audit import write_event
from app.services.cache import invalidate
from app.services.orders import create_order as create_order_service
from app.services.orders import get_order_or_404, list_orders, ship_order
from app.services.serializers import order_to_read

router = APIRouter(prefix="/orders", tags=["orders"])


@router.get("", response_model=list[OrderRead])
def read_orders(
    db: Session = Depends(get_db),
    _: dict[str, str] = Depends(require_roles("admin", "operator")),
) -> list[dict]:
    return [order_to_read(order) for order in list_orders(db)]


@router.get("/{order_id}", response_model=OrderRead)
def read_order(
    order_id: int,
    db: Session = Depends(get_db),
    _: dict[str, str] = Depends(require_roles("admin", "operator")),
) -> dict:
    return order_to_read(get_order_or_404(db, order_id))


@router.post("", response_model=OrderRead, status_code=status.HTTP_201_CREATED)
async def create_order(
    payload: OrderCreate,
    db: Session = Depends(get_db),
    _: dict[str, str] = Depends(require_roles("admin", "operator")),
) -> dict:
    order = create_order_service(db, payload)
    db.commit()
    invalidate("dashboard:kpi")
    await write_event("create", "order", order.id, f"Создан заказ {order.number}")
    return order_to_read(order)


@router.post("/{order_id}/ship", response_model=OrderRead)
async def ship(
    order_id: int,
    db: Session = Depends(get_db),
    _: dict[str, str] = Depends(require_roles("admin", "operator")),
) -> dict:
    order = ship_order(db, order_id)
    db.commit()
    invalidate("dashboard:kpi")
    await write_event("ship", "order", order.id, f"Заказ {order.number} отгружен")
    return order_to_read(order)
