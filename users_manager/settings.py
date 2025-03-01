from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    postgres_user: str = Field(default="postgres")
    postgres_password: str = Field(default="password")
    postgres_host: str = Field(default="user-db")
    postgres_port: str = Field(default="5432")
    postgres_name: str = Field(default="employee_manager_db")
    tenant_domain: str
    database_id_connection: str
    management_api_token: str
    client_id: str
    organization_identifier: str
    mail_gun_api_key: str

settings = Settings()
