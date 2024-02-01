from pydantic import PostgresDsn, RedisDsn, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """A class that contains data from an environment file"""

    bot_token: SecretStr
    pg_dsn: PostgresDsn
    redis_dsn: RedisDsn

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")
