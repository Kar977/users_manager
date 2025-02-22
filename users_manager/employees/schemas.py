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
    given_name: Optional[str] = None
    family_name: Optional[str] = None
    name: Optional[str] = None
    nickname: Optional[str] = None
    picture: Optional[str] = None
    verify_email: Optional[bool] = None
    verify_phone_number: Optional[bool] = None
    password: Optional[str] = None
    username: Optional[str] = None


class NewMember(BaseModel):
    email: str
    organization_id: str


class ModifyClientType(BaseModel):  # ToDo skasowac
    client_id: str
    app_type: str


class ListOrganizations(BaseModel):
    tenant_domain: str


class AddRolesToUser(BaseModel):
    user_id: str
    organization: str
    roles: list


class RemoveUserFromOrganization(BaseModel):
    user_id: str
    organization_id: str
