"""Application configuration using pydantic-settings."""
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    database_url: str
    cors_origins: str = "http://localhost:3000"
    environment: str = "development"
    kafka_enabled: bool = False
    kafka_bootstrap_servers: str = "localhost:9092"
    jwt_secret_key: str = "change-me-in-production"
    jwt_algorithm: str = "HS256"
    jwt_expire_minutes: int = 1440

    model_config = SettingsConfigDict(env_file=".env", case_sensitive=False)


settings = Settings()
