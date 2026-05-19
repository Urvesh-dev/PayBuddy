from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    app_name: str = "PayBuddy Salary Management"
    debug: bool = False
    api_v1_prefix: str = "/api/v1"
    database_url: str = "postgresql://paybuddy:paybuddy@localhost:5432/paybuddy"
    cors_origins: str = "http://localhost:5173,http://localhost:3000"
    log_level: str = "INFO"
    default_page_size: int = 20
    max_page_size: int = 100

    @property
    def cors_origin_list(self) -> list[str]:
        return [o.strip() for o in self.cors_origins.split(",") if o.strip()]


@lru_cache
def get_settings() -> Settings:
    return Settings()
