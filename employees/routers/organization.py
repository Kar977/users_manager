from fastapi import APIRouter

from employees.schemas import (
    CreateOrganization,
    OrganizationName,
    OrganizationIdentifier,
    ModifyOrganization,
    ModifyClientType,
)
from employees.services.organization import organization_manager_obj

router = APIRouter()


@router.get("/organization", status_code=200)
async def get_organization(organization_request: OrganizationName):
    return await organization_manager_obj.get_organization_by_name(
        organization_request.name
    )


@router.post("/organization", status_code=201)
async def create_new_organization(organization_request: CreateOrganization):
    return await organization_manager_obj.create_organization(
        organization_request.name, organization_request.display_name
    )


@router.delete("/organization", status_code=204)
async def delete_organization(organization_request: OrganizationIdentifier):
    return await organization_manager_obj.delete_organization_by_identifier(
        organization_request.identifier
    )


@router.put("/organization", status_code=200)
async def modify_organization_router(organization_request: ModifyOrganization):
    return await organization_manager_obj.modify_organization(
        identifier=organization_request.identifier,
        name=organization_request.name,
        display_name=organization_request.display_name,
        logo_url=organization_request.logo_url,
        primary_color=organization_request.primary_color,
        background_color=organization_request.background_color,
    )


@router.patch("/change_client_type", status_code=200)
async def change_client_type(user_request: ModifyClientType):
    return await organization_manager_obj.change_client_type(
        user_request.client_id, user_request.app_type
    )
