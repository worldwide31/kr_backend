from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.models import Company, CompanyRole, Order, OrderItem, OrderStatus, Product, Warehouse
from app.schemas.order import OrderCreate
from app.services.inventory import reserve_stock, ship_reserved_stock
from app.services.numbers import make_number


def list_orders(db: Session) -> list[Order]:
    return list(
        db.scalars(
            select(Order)
            .options(
                selectinload(Order.customer),
                selectinload(Order.items).selectinload(OrderItem.product),
                selectinload(Order.items).selectinload(OrderItem.warehouse),
            )
            .order_by(Order.created_at.desc())
        )
    )


def get_order_or_404(db: Session, order_id: int) -> Order:
    order = db.scalar(
        select(Order)
        .where(Order.id == order_id)
        .options(
            selectinload(Order.customer),
            selectinload(Order.items).selectinload(OrderItem.product),
            selectinload(Order.items).selectinload(OrderItem.warehouse),
        )
    )
    if not order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Заказ не найден")
    return order


def create_order(db: Session, payload: OrderCreate) -> Order:
    customer = db.get(Company, payload.customer_id)
    if not customer or customer.role not in {CompanyRole.customer, CompanyRole.both}:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Выберите клиента")

    order = Order(number="draft", customer_id=payload.customer_id, delivery_city=payload.delivery_city, comment=payload.comment)
    db.add(order)
    db.flush()
    order.number = make_number("ORD", order.id)

    for item in payload.items:
        if not db.get(Product, item.product_id):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Товар {item.product_id} не найден")
        if not db.get(Warehouse, item.warehouse_id):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Склад {item.warehouse_id} не найден")
        reserve_stock(db, item.product_id, item.warehouse_id, item.quantity)
        db.add(
            OrderItem(
                order_id=order.id,
                product_id=item.product_id,
                warehouse_id=item.warehouse_id,
                quantity=item.quantity,
                unit_price=item.unit_price,
            )
        )

    order.status = OrderStatus.confirmed
    db.flush()
    return get_order_or_404(db, order.id)


def ship_order(db: Session, order_id: int) -> Order:
    order = get_order_or_404(db, order_id)
    if order.status != OrderStatus.confirmed:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Отгрузить можно только подтвержденный заказ")
    for item in order.items:
        ship_reserved_stock(db, item.product_id, item.warehouse_id, item.quantity)
    order.status = OrderStatus.shipped
    db.flush()
    return get_order_or_404(db, order.id)

