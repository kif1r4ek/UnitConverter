from pydantic_settings import BaseSettings
from typing import Literal

class Settings(BaseSettings):
    PROJECT_NAME: str = "UnitConverter"
    PROJECT_VERSION: str = "1.0.0"
    DEBUG: bool = False

    LOG_LEVEL: Literal["DEBUG", "INFO", "WARNING", "ERROR"] = "INFO"
    LOG_FILE: str = "app/core/logs/app.log"
    LOG_ERROR_FILE: str = "app/core/logs/error.log"
    LOG_FORMAT: Literal["json", "console"] = "json"
    LOG_SIZE: int = 10_000_000
    LOG_BACKUP_COUNT: int = 5

    HOST: str = "0.0.0.0"
    PORT: int = 8000

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()