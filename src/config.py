from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Literal


class Settings(BaseSettings):

    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASS: str
    DB_NAME: str

    SECRET_KEY: str
    ALGORITHM: str
    API_KEY: str

    @property
    def DATABASE_URL(self):

        return f"postgresql+asyncpg://myuser:mypassword@localhost:5432/mydatabase"

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
