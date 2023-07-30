import secrets
from typing import Any, Dict, List, Optional
from pydantic import AnyHttpUrl, BaseSettings, validator, PostgresDsn
from dotenv import load_dotenv
load_dotenv()

class Settings(BaseSettings):
    #REDIS_BROKER_URL: str
    #REDIS_BACKEND_URL: str
    REDIS_HOST: str
    REDIS_PASSWORD: str
    POSTGRES_SERVER: str = "10.101.14.21:5432"
    POSTGRES_USER: str = 'postgres'
    POSTGRES_PASSWORD: str = 'postgres'
    POSTGRES_DB: str = 'app'
    SQLALCHEMY_DATABASE_URI: Optional[PostgresDsn] = None

    @validator("SQLALCHEMY_DATABASE_URI")
    def assemble_db_connection(cls, v: Optional[str], values: Dict[str, Any]) -> Any:
        if isinstance(v, str):
            return v
        return PostgresDsn.build(
            scheme="postgresql",
            user=values.get('POSTGRES_USER'),
            password=values.get("POSTGRES_PASSWORD"),
            host=values.get("POSTGRES_SERVER"),
            path=f"/{values.get('POSTGRES_DB') or ''}",
        )
settings = Settings()