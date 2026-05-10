from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models import Product
from app.schemas.product import ProductCreate, ProductRead
from app.services.audit import write_event
from app.services.cache import invalidate

router = APIRouter(prefix="/products", tags=["products"])


@router.get("", response_model=list[ProductRead])
def list_products(db: Session = Depends(get_db)) -> list[Product]:
    return list(db.scalars(select(Product).order_by(Product.name)))


@router.post("", response_model=ProductRead, status_code=status.HTTP_201_CREATED)
async def create_product(payload: ProductCreate, db: Session = Depends(get_db)) -> Product:
    duplicate = db.scalar(select(Product).where(Product.sku == payload.sku))
    if duplicate:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Товар с таким SKU уже есть в каталоге. Измените артикул или используйте существующую позицию.",
        )
    product = Product(**payload.model_dump())
    db.add(product)
    db.commit()
    db.refresh(product)
    invalidate("dashboard:kpi")
    await write_event("create", "product", product.id, f"Добавлен товар {product.name}")
    return product
