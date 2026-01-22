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

    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_DB: int = 0
    REDIS_PASSWORD: str | None = None

    REDIS_MAX_CONNECTIONS: int = 10
    REDIS_DECODE_RESPONSES: bool = True

    @property
    def REDIS_URL(self):
        if self.REDIS_PASSWORD:
            return (
                f"redis://:{self.REDIS_PASSWORD}"
                f"@{self.REDIS_HOST}:{self.REDIS_PORT}/{self.REDIS_DB}"
            )
        return f"redis://{self.REDIS_HOST}:{self.REDIS_PORT}/{self.REDIS_DB}"


    HISTORY_TTL: int = 86400
    MAX_HISTORY_ITEMS: int = 10

    HOST: str = "0.0.0.0"
    PORT: int = 8000

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()