from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import InventoryItem


def get_or_create_inventory(db: Session, product_id: int, warehouse_id: int) -> InventoryItem:
    item = db.scalar(
        select(InventoryItem).where(
            InventoryItem.product_id == product_id,
            InventoryItem.warehouse_id == warehouse_id,
        )
    )
    if item:
        return item
    item = InventoryItem(product_id=product_id, warehouse_id=warehouse_id, quantity=0, reserved=0)
    db.add(item)
    db.flush()
    return item


def reserve_stock(db: Session, product_id: int, warehouse_id: int, quantity: int) -> None:
    item = get_or_create_inventory(db, product_id, warehouse_id)
    available = item.quantity - item.reserved
    if available < quantity:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Недостаточно остатка товара {product_id} на складе {warehouse_id}: доступно {available}",
        )
    item.reserved += quantity


def ship_reserved_stock(db: Session, product_id: int, warehouse_id: int, quantity: int) -> None:
    item = get_or_create_inventory(db, product_id, warehouse_id)
    if item.reserved < quantity:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Нельзя отгрузить больше резерва")
    item.reserved -= quantity
    item.quantity -= quantity


def receive_stock(db: Session, product_id: int, warehouse_id: int, quantity: int) -> None:
    item = get_or_create_inventory(db, product_id, warehouse_id)
    item.quantity += quantity

