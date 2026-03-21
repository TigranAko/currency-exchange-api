from pathlib import Path

from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

path_to_env = f"{Path().absolute()}/../.env"


class ConfigBase(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=path_to_env, env_file_encoding="utf-8", extra="ignore"
    )


class ConfigAuth(ConfigBase):
    JWT_SECRET_KEY: SecretStr


class ConfigCurrencyExchange(ConfigBase):
    CURRENCY_EXCHANGE_API_KEY: SecretStr


class ConfigDB(ConfigBase):
    DB_URL: SecretStr


config_db = ConfigDB()
