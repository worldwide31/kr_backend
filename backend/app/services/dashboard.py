from decimal import Decimal

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models import Company, InventoryItem, Order, OrderItem, OrderStatus, Product, Supply, SupplyStatus, Warehouse
from app.services.cache import cached_json


def dashboard_kpi(db: Session) -> dict:
    def load() -> dict:
        inventory_units = db.scalar(select(func.coalesce(func.sum(InventoryItem.quantity), 0))) or 0
        reserved_units = db.scalar(select(func.coalesce(func.sum(InventoryItem.reserved), 0))) or 0
        low_stock_items = (
            db.scalar(
                select(func.count())
                .select_from(InventoryItem)
                .join(Product)
                .where((InventoryItem.quantity - InventoryItem.reserved) <= Product.min_stock)
            )
            or 0
        )
        revenue = (
            db.scalar(
                select(func.coalesce(func.sum(OrderItem.quantity * OrderItem.unit_price), Decimal("0.00")))
                .select_from(OrderItem)
                .join(Order)
                .where(Order.status != OrderStatus.cancelled)
            )
            or Decimal("0.00")
        )
        return {
            "companies": db.scalar(select(func.count(Company.id))) or 0,
            "products": db.scalar(select(func.count(Product.id))) or 0,
            "warehouses": db.scalar(select(func.count(Warehouse.id))) or 0,
            "active_orders": db.scalar(select(func.count(Order.id)).where(Order.status == OrderStatus.confirmed)) or 0,
            "planned_supplies": db.scalar(select(func.count(Supply.id)).where(Supply.status == SupplyStatus.planned)) or 0,
            "inventory_units": inventory_units,
            "reserved_units": reserved_units,
            "low_stock_items": low_stock_items,
            "order_revenue": revenue,
        }

    return cached_json("dashboard:kpi", load, ttl_seconds=30)

