"""
Configuration Management
Environment-based settings using Pydantic Settings
"""

from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.

    Environment variables are loaded from .env file or system environment.
    """

    # Database Configuration
    DATABASE_URL: str

    # Authentication Configuration
    BETTER_AUTH_SECRET: str

    # CORS Configuration
    CORS_ORIGINS: str = "http://localhost:3000"

    # Optional Configuration
    ENVIRONMENT: str = "development"

    # JWT Configuration
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRATION_MINUTES: int = 1440  # 24 hours

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore"
    )

    def get_cors_origins(self) -> List[str]:
        """
        Parse CORS_ORIGINS string into list of origins.
        Supports comma-separated values.
        """
        if isinstance(self.CORS_ORIGINS, str):
            return [origin.strip() for origin in self.CORS_ORIGINS.split(",")]
        return self.CORS_ORIGINS


# Global settings instance
settings = Settings()
