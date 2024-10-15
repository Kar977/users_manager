import os

from dotenv import load_dotenv

load_dotenv()


class Settings:
    TENANT_DOMAIN = os.getenv("TENANT_DOMAIN")
    DATABASE_ID_CONNECTION = os.getenv("DATABASE_ID_CONNECTION")
    MANAGEMENT_API_TOKEN = os.getenv("MANAGEMENT_API_TOKEN")
