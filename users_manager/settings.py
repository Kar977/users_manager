from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=Path(__file__).parent / ".env")
    postgres_user: str = Field(default="postgres")
    postgres_password: str = Field(default="password")
    postgres_host: str = Field(default="user-db")
    postgres_port: str = Field(default="5432")
    postgres_name: str = Field(default="employee_manager_db")
    tenant_domain: str = Field()
    database_id_connection: str = Field()
    management_api_token: str = Field()
    client_id: str = Field()
    organization_identifier: str = Field()
    mail_gun_api_key: str = Field()


settings = Settings()
