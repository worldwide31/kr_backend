from decimal import Decimal

from app.schemas.common import ORMModel


class DashboardKpi(ORMModel):
    companies: int
    products: int
    warehouses: int
    active_orders: int
    planned_supplies: int
    inventory_units: int
    reserved_units: int
    low_stock_items: int
    order_revenue: Decimal


class ActivityEvent(ORMModel):
    id: str
    action: str
    entity_type: str
    entity_id: str
    message: str
    created_at: str

