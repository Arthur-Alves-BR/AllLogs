from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    access_token_expire_minutes: int
    refresh_token_expire_days: int
    secret_key: str

    model_config = SettingsConfigDict(env_file=".env", env_nested_delimiter="__")


config = Settings()
