from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=Path(__file__).parent / ".env")
    postgres_user: str = Field()
    postgres_password: str = Field()
    postgres_host: str = Field()
    postgres_port: str = Field()
    postgres_name: str = Field()
    tenant_domain: str = Field()
    database_id_connection: str = Field()
    management_api_token: str = Field()
    client_id: str = Field()
    organization_identifier: str = Field()
    mail_gun_api_key: str = Field()


settings = Settings()
