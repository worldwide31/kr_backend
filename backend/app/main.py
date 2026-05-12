from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import auth, companies, dashboard, events, orders, products, seed, supplies, warehouses
from app.core.config import settings
from app.db.session import Base, engine


def create_app() -> FastAPI:
    app = FastAPI(
        title="MuzFlow API",
        description="API веб-сервиса управления поставками и заказами для оптовых компаний.",
        version="1.0.0",
        docs_url="/api/docs",
        openapi_url="/api/openapi.json",
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.on_event("startup")
    def on_startup() -> None:
        Base.metadata.create_all(bind=engine)

    app.include_router(auth.router, prefix="/api")
    app.include_router(dashboard.router, prefix="/api")
    app.include_router(companies.router, prefix="/api")
    app.include_router(products.router, prefix="/api")
    app.include_router(warehouses.router, prefix="/api")
    app.include_router(orders.router, prefix="/api")
    app.include_router(supplies.router, prefix="/api")
    app.include_router(events.router, prefix="/api")
    app.include_router(seed.router, prefix="/api")

    @app.get("/api/health", tags=["system"])
    def healthcheck() -> dict[str, str]:
        return {"status": "ok"}

    return app


app = create_app()
