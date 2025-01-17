from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
  aws_access_id: str
  aws_secret_key: str
  aws_region: str

  model_config = SettingsConfigDict(env_file=".env")

@lru_cache(maxsize=1)
def get_settings():
    return Settings()