import enum
from datetime import datetime
from decimal import Decimal

from sqlalchemy import DateTime, Enum, ForeignKey, Numeric, String, Text, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.session import Base


class CompanyRole(str, enum.Enum):
    customer = "customer"
    supplier = "supplier"
    both = "both"


class OrderStatus(str, enum.Enum):
    draft = "draft"
    confirmed = "confirmed"
    shipped = "shipped"
    cancelled = "cancelled"


class SupplyStatus(str, enum.Enum):
    planned = "planned"
    received = "received"
    cancelled = "cancelled"


class Company(Base):
    __tablename__ = "companies"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(180), nullable=False, unique=True)
    inn: Mapped[str] = mapped_column(String(12), nullable=False, unique=True)
    role: Mapped[CompanyRole] = mapped_column(Enum(CompanyRole), nullable=False)
    contact_name: Mapped[str | None] = mapped_column(String(120))
    email: Mapped[str | None] = mapped_column(String(180))
    phone: Mapped[str | None] = mapped_column(String(40))
    address: Mapped[str | None] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    orders: Mapped[list["Order"]] = relationship(back_populates="customer")
    supplies: Mapped[list["Supply"]] = relationship(back_populates="supplier")


class Product(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(primary_key=True)
    sku: Mapped[str] = mapped_column(String(64), nullable=False, unique=True)
    name: Mapped[str] = mapped_column(String(180), nullable=False)
    category: Mapped[str] = mapped_column(String(120), nullable=False)
    unit: Mapped[str] = mapped_column(String(32), nullable=False, default="шт")
    purchase_price: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False, default=0)
    sale_price: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False, default=0)
    min_stock: Mapped[int] = mapped_column(nullable=False, default=0)

    inventory: Mapped[list["InventoryItem"]] = relationship(back_populates="product")


class Warehouse(Base):
    __tablename__ = "warehouses"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(160), nullable=False, unique=True)
    city: Mapped[str] = mapped_column(String(100), nullable=False)
    address: Mapped[str] = mapped_column(Text, nullable=False)
    manager: Mapped[str | None] = mapped_column(String(120))

    inventory: Mapped[list["InventoryItem"]] = relationship(back_populates="warehouse")


class InventoryItem(Base):
    __tablename__ = "inventory_items"
    __table_args__ = (UniqueConstraint("product_id", "warehouse_id", name="uq_inventory_product_warehouse"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"), nullable=False)
    warehouse_id: Mapped[int] = mapped_column(ForeignKey("warehouses.id"), nullable=False)
    quantity: Mapped[int] = mapped_column(nullable=False, default=0)
    reserved: Mapped[int] = mapped_column(nullable=False, default=0)

    product: Mapped[Product] = relationship(back_populates="inventory")
    warehouse: Mapped[Warehouse] = relationship(back_populates="inventory")


class Order(Base):
    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(primary_key=True)
    number: Mapped[str] = mapped_column(String(40), nullable=False, unique=True)
    customer_id: Mapped[int] = mapped_column(ForeignKey("companies.id"), nullable=False)
    status: Mapped[OrderStatus] = mapped_column(Enum(OrderStatus), nullable=False, default=OrderStatus.draft)
    delivery_city: Mapped[str] = mapped_column(String(100), nullable=False)
    comment: Mapped[str | None] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    customer: Mapped[Company] = relationship(back_populates="orders")
    items: Mapped[list["OrderItem"]] = relationship(cascade="all, delete-orphan", back_populates="order")


class OrderItem(Base):
    __tablename__ = "order_items"

    id: Mapped[int] = mapped_column(primary_key=True)
    order_id: Mapped[int] = mapped_column(ForeignKey("orders.id"), nullable=False)
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"), nullable=False)
    warehouse_id: Mapped[int] = mapped_column(ForeignKey("warehouses.id"), nullable=False)
    quantity: Mapped[int] = mapped_column(nullable=False)
    unit_price: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)

    order: Mapped[Order] = relationship(back_populates="items")
    product: Mapped[Product] = relationship()
    warehouse: Mapped[Warehouse] = relationship()


class Supply(Base):
    __tablename__ = "supplies"

    id: Mapped[int] = mapped_column(primary_key=True)
    number: Mapped[str] = mapped_column(String(40), nullable=False, unique=True)
    supplier_id: Mapped[int] = mapped_column(ForeignKey("companies.id"), nullable=False)
    status: Mapped[SupplyStatus] = mapped_column(Enum(SupplyStatus), nullable=False, default=SupplyStatus.planned)
    eta: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    supplier: Mapped[Company] = relationship(back_populates="supplies")
    items: Mapped[list["SupplyItem"]] = relationship(cascade="all, delete-orphan", back_populates="supply")


class SupplyItem(Base):
    __tablename__ = "supply_items"

    id: Mapped[int] = mapped_column(primary_key=True)
    supply_id: Mapped[int] = mapped_column(ForeignKey("supplies.id"), nullable=False)
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"), nullable=False)
    warehouse_id: Mapped[int] = mapped_column(ForeignKey("warehouses.id"), nullable=False)
    quantity: Mapped[int] = mapped_column(nullable=False)
    purchase_price: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)

    supply: Mapped[Supply] = relationship(back_populates="items")
    product: Mapped[Product] = relationship()
    warehouse: Mapped[Warehouse] = relationship()

