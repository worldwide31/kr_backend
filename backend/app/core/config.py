from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    database_url: str = Field(
        default="postgresql+psycopg://supplyflow:supplyflow@localhost:5432/supplyflow",
        alias="DATABASE_URL",
    )
    mongo_url: str = Field(default="mongodb://localhost:27017", alias="MONGO_URL")
    mongo_db: str = Field(default="supplyflow", alias="MONGO_DB")
    redis_url: str = Field(default="redis://localhost:6379/0", alias="REDIS_URL")
    cors_origins_raw: str = Field(
        default="http://localhost,http://localhost:5173",
        alias="CORS_ORIGINS",
    )

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    @property
    def cors_origins(self) -> list[str]:
        return [origin.strip() for origin in self.cors_origins_raw.split(",") if origin.strip()]


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()

