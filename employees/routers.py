from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse

from employees.schemas import CreateOrganization, OrganizationName, OrganizationIdentifier, ModifyOrganization
from employees.services.crud import organization_manager_obj

router = APIRouter()

@router.get("/text")
async def view_text(request: Request):
    return JSONResponse("its ok")

@router.get("/organization")
async def get_organization(organization_request: OrganizationName):

    get_details = organization_manager_obj.get_organization_by_name(organization_request.name)

    return get_details


@router.post("/organization")
async def create_new_organization(organization_request: CreateOrganization):

    print("parametry w params req: ", organization_request.name, organization_request.display_name, )

    create_new_organization = organization_manager_obj.create_organization(organization_request.name,
                                                                           organization_request.display_name)

    return create_new_organization

@router.delete("/organization")
async def delete_organization(organization_request: OrganizationIdentifier):

    delete = organization_manager_obj.delete_organization_by_identifier(organization_request.identifier)

    return delete

@router.put("/organization")
async def modify_organization_router(organization_request: ModifyOrganization):
    modify = organization_manager_obj.modify_organization(
        identifier=organization_request.identifier,
        name=organization_request.name if organization_request.name is not None else None,
        display_name=organization_request.display_name if organization_request.display_name is not None else None,
        logo_url=organization_request.logo_url if organization_request.logo_url is not None else None,
        primary_color=organization_request.primary_color if organization_request.primary_color is not None else None,
        background_color=organization_request.background_color if organization_request.background_color is not None else None
    )

    return modify