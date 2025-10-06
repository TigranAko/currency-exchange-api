from pydantic_settings import SettingsConfigDict, BaseSettings
from pydantic import SecretStr


class ConfigBase(BaseSettings):
    model_config= SettingsConfigDict(env_file="./.env", env_file_encoding="utf-8", extra="ignore")


class ConfigAuth(ConfigBase):
    JWT_SECRET_KEY: SecretStr


class ConfigCurrencyExchange(ConfigBase):
    CURRENCY_EXCHANGE_API_KEY: SecretStr





