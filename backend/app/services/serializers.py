from decimal import Decimal

from app.models import InventoryItem, Order, OrderItem, Supply, SupplyItem


def order_item_to_read(item: OrderItem) -> dict:
    total = item.unit_price * item.quantity
    return {
        "id": item.id,
        "product_id": item.product_id,
        "warehouse_id": item.warehouse_id,
        "product_name": item.product.name,
        "warehouse_name": item.warehouse.name,
        "quantity": item.quantity,
        "unit_price": item.unit_price,
        "total": total,
    }


def order_to_read(order: Order) -> dict:
    items = [order_item_to_read(item) for item in order.items]
    return {
        "id": order.id,
        "number": order.number,
        "customer_id": order.customer_id,
        "customer_name": order.customer.name,
        "status": order.status,
        "delivery_city": order.delivery_city,
        "comment": order.comment,
        "created_at": order.created_at,
        "total": sum((item["total"] for item in items), Decimal("0.00")),
        "items": items,
    }


def supply_item_to_read(item: SupplyItem) -> dict:
    total = item.purchase_price * item.quantity
    return {
        "id": item.id,
        "product_id": item.product_id,
        "warehouse_id": item.warehouse_id,
        "product_name": item.product.name,
        "warehouse_name": item.warehouse.name,
        "quantity": item.quantity,
        "purchase_price": item.purchase_price,
        "total": total,
    }


def supply_to_read(supply: Supply) -> dict:
    items = [supply_item_to_read(item) for item in supply.items]
    return {
        "id": supply.id,
        "number": supply.number,
        "supplier_id": supply.supplier_id,
        "supplier_name": supply.supplier.name,
        "status": supply.status,
        "eta": supply.eta,
        "created_at": supply.created_at,
        "total": sum((item["total"] for item in items), Decimal("0.00")),
        "items": items,
    }


def inventory_to_read(item: InventoryItem) -> dict:
    return {
        "id": item.id,
        "product_id": item.product_id,
        "warehouse_id": item.warehouse_id,
        "product_name": item.product.name,
        "sku": item.product.sku,
        "warehouse_name": item.warehouse.name,
        "quantity": item.quantity,
        "reserved": item.reserved,
        "available": item.quantity - item.reserved,
        "min_stock": item.product.min_stock,
    }

