from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    app_name: str = "GovPath"
    api_v1_prefix: str = "/api"
    secret_key: str = "change-me-in-production"
    database_url: str = "postgresql+psycopg2://postgres:postgres@localhost:5432/govpath"


settings = Settings()
