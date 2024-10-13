from pydantic import BaseModel
from typing import Optional

class CreateOrganization(BaseModel):
    name: str
    display_name: str

class OrganizationName(BaseModel):
    name: str

class OrganizationIdentifier(BaseModel):
    identifier: str

class ModifyOrganization(BaseModel):
    identifier: str
    name: Optional[str] = None
    display_name: Optional[str] =None
    logo_url: Optional[str] = None
    primary_color: Optional[str] = None
    background_color: Optional[str] = None
