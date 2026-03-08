import json
from typing import Literal

from pydantic import SecretStr, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    database_hostname: str
    database_port: int
    database_password: str
    database_name: str
    database_username: str
    secret_key: SecretStr
    algorithm: str
    access_token_expire_minutes: int
    environment: Literal["dev", "prod", "test"] = "dev"
    debug: bool = False
    sql_echo: bool = False
    
    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
