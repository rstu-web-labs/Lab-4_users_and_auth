from pathlib import Path
from typing import Literal

from dotenv import load_dotenv
from pydantic import PositiveInt
from pydantic_settings import BaseSettings

from app.core.constants.base import LogLevelTypes

load_dotenv()


APP_DESC = """---
### Описание

Сервис для сокращения ссылок

---

### Доступ

Сервис имеет несколько эндпоинтов.

Для эндпоинтов, требующих авторизации, требуется указывать секретный ключ в заголовках запроса в следующем формате:

`Authorization: Bearer {token}`
"""


BASE_DIR = Path(__file__).resolve().parent.parent.parent
MEDIA_DIR = BASE_DIR / "media"
STATIC_DIR = BASE_DIR / "static"

STATIC_DIR.mkdir(exist_ok=True)
MEDIA_DIR.mkdir(exist_ok=True)


class LoggingSettings(BaseSettings):
    log_level: str = LogLevelTypes.INFO


class DatabaseSettings(BaseSettings):
    db_postgres_host: str
    db_postgres_port: str = '5432'
    db_postgres_name: str
    db_postgres_username: str
    db_postgres_password: str
    db_postgres_timeout: PositiveInt = 5
    db_postgres_driver: Literal["psycopg", "pycopg2"] = "psycopg"


    @property
    def postgres_host_url(self):
        return (
            f"postgresql+{self.db_postgres_driver}://"
            f"{self.db_postgres_username}:{self.db_postgres_password}"
            f"@{self.db_postgres_host}:{self.db_postgres_port}/"
        )

    @property
    def postgres_database_url(self):
        return f"{self.postgres_host_url}{self.db_postgres_name}"


class ExtraSettings(BaseSettings): ...

class AuthSettings(BaseSettings):
    secret_key: str
    algorithm: str
    access_token_expire_minutes: PositiveInt
    refresh_token_expire_minutes: PositiveInt

class Settings(DatabaseSettings, LoggingSettings, ExtraSettings, AuthSettings):
    app_title: str = "Short Url"
    app_description: str = APP_DESC
    mock_external_services: bool = False
    local: bool = False


app_settings = Settings()

