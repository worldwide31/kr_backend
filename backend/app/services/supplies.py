from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.models import Company, CompanyRole, Product, Supply, SupplyItem, SupplyStatus, Warehouse
from app.schemas.supply import SupplyCreate
from app.services.inventory import receive_stock
from app.services.numbers import make_number


def list_supplies(db: Session) -> list[Supply]:
    return list(
        db.scalars(
            select(Supply)
            .options(
                selectinload(Supply.supplier),
                selectinload(Supply.items).selectinload(SupplyItem.product),
                selectinload(Supply.items).selectinload(SupplyItem.warehouse),
            )
            .order_by(Supply.created_at.desc())
        )
    )


def get_supply_or_404(db: Session, supply_id: int) -> Supply:
    supply = db.scalar(
        select(Supply)
        .where(Supply.id == supply_id)
        .options(
            selectinload(Supply.supplier),
            selectinload(Supply.items).selectinload(SupplyItem.product),
            selectinload(Supply.items).selectinload(SupplyItem.warehouse),
        )
    )
    if not supply:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Поставка не найдена")
    return supply


def create_supply(db: Session, payload: SupplyCreate) -> Supply:
    supplier = db.get(Company, payload.supplier_id)
    if not supplier or supplier.role not in {CompanyRole.supplier, CompanyRole.both}:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Выберите поставщика")

    supply = Supply(number="draft", supplier_id=payload.supplier_id, eta=payload.eta)
    db.add(supply)
    db.flush()
    supply.number = make_number("SUP", supply.id)

    for item in payload.items:
        if not db.get(Product, item.product_id):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Товар {item.product_id} не найден")
        if not db.get(Warehouse, item.warehouse_id):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Склад {item.warehouse_id} не найден")
        db.add(
            SupplyItem(
                supply_id=supply.id,
                product_id=item.product_id,
                warehouse_id=item.warehouse_id,
                quantity=item.quantity,
                purchase_price=item.purchase_price,
            )
        )

    db.flush()
    return get_supply_or_404(db, supply.id)


def receive_supply(db: Session, supply_id: int) -> Supply:
    supply = get_supply_or_404(db, supply_id)
    if supply.status != SupplyStatus.planned:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Поставка уже обработана")
    for item in supply.items:
        receive_stock(db, item.product_id, item.warehouse_id, item.quantity)
    supply.status = SupplyStatus.received
    db.flush()
    return get_supply_or_404(db, supply.id)

