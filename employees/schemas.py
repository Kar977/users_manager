from typing import Optional

from pydantic import BaseModel


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
    display_name: Optional[str] = None
    logo_url: Optional[str] = None
    primary_color: Optional[str] = None
    background_color: Optional[str] = None


class CreateUser(BaseModel):
    email: str
    name: str
    family_name: str
    username: str


class SetUserPasswordEmail(BaseModel):
    user_email: str


class DeleteUserAccount(BaseModel):
    email: str


class ModifyUser(BaseModel):
    user_id: str
    blocked: Optional[bool] = None
    email_verified: Optional[bool] = None
    email: Optional[str] = None
    phone_number: Optional[str] = None
    phone_verified: Optional[bool] = None
    user_metadata: Optional[dict] = None
    app_metadata: Optional[dict] = None
    given_name: Optional[str] = None
    family_name: Optional[str] = None
    name: Optional[str] = None
    nickname: Optional[str] = None
    picture: Optional[str] = None
    verify_email: Optional[bool] = None
    verify_phone_number: Optional[bool] = None
    password: Optional[str] = None
    connection: Optional[str] = None
    client_id: Optional[str] = None
    username: Optional[str] = None


class NewMember(BaseModel):
    email: str


class ModifyClientType(BaseModel):
    client_id: str
    app_type: str
