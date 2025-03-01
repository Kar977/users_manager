import json

import aiohttp
from fastapi import HTTPException
from settings import settings


async def make_request_with_error_handling(
    method: str, url: str, headers=None, data=None
):
    try:
        async with aiohttp.ClientSession() as session:
            response = await session.request(method, url, headers=headers, data=data)
            response.raise_for_status()

            result = {
                "status": response.status,
                "headers": dict(response.headers),
                "body": await response.text(),
            }

            return result
    except aiohttp.ClientResponseError as http_err:
        raise HTTPException(status_code=http_err.status, detail=http_err.message)
    except aiohttp.ClientConnectionError as conn_err:
        raise HTTPException(conn_err)
    except aiohttp.ClientError as client_err:
        raise HTTPException(client_err)
    except Exception as err:
        raise HTTPException(status_Code=500, detail=err)


class OrganizationManager:

    async def create_organization(
        self,
        name: str,
        display_name: str,
        primary_color: str = "#eb4034",
        background_color: str = "#e0b9b6",
    ):

        url = f"https://{settings.tenant_domain}.eu.auth0.com/api/v2/organizations"

        payload = json.dumps(
            {
                "name": f"{name}",
                "display_name": f"{display_name}",
                "branding": {
                    "colors": {
                        "primary": f"{primary_color}",
                        "page_background": f"{background_color}",
                    }
                },
                "metadata": {},
                "enabled_connections": [
                    {
                        "connection_id": f"{settings.database_id_connection}",
                        "assign_membership_on_login": True,
                        "show_as_button": True,
                        "is_signup_enabled": True,
                    }
                ],
            }
        )
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": f"Bearer {settings.management_api_token}",
        }

        response = await make_request_with_error_handling(
            "POST", url, headers=headers, data=payload
        )

        return response.get("body")

    async def get_organization_by_name(self, name: str = "nowy-polski-salon"):

        url = f"https://{settings.tenant_domain}.eu.auth0.com/api/v2/organizations/name/{name}"

        payload = {}
        headers = {
            "Accept": "application/json",
            "Authorization": f"Bearer {settings.management_api_token}",
        }

        response = await make_request_with_error_handling(
            "GET", url, headers=headers, data=payload
        )
        return response.get("body")

    async def delete_organization_by_identifier(self, identifier: str):

        url = f"https://{settings.tenant_domain}.eu.auth0.com/api/v2/organizations/{identifier}"

        payload = {}
        headers = {"Authorization": f"Bearer {settings.management_api_token}"}

        response = await make_request_with_error_handling(
            "DELETE", url, headers=headers, data=payload
        )
        return response.get("body")

    async def modify_organization(
        self,
        identifier: str,
        name: str = None,
        display_name: str = None,
        logo_url: str = None,
        primary_color: str = None,
        background_color: str = None,
    ):

        url = f"https://{settings.tenant_domain}.eu.auth0.com/api/v2/organizations/{identifier}"

        payload = {
            "name": name,
            "display_name": display_name,
            "branding": (
                {
                    "logo_url": logo_url,
                    "colors": (
                        {"primary": primary_color, "page_background": background_color}
                        if primary_color or background_color
                        else {}
                    ),
                }
                if logo_url or primary_color or background_color
                else {}
            ),
        }

        payload = {k: v for k, v in payload.items() if v is not None}

        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": f"Bearer {settings.management_api_token}",
        }

        response = await make_request_with_error_handling(
            "PATCH", url, headers=headers, data=json.dumps(payload)
        )
        return response.get("body")

    async def change_client_type(self, client_id: str, app_type: str):
        url = (
            f"https://{settings.tenant_domain}.eu.auth0.com/api/v2/clients/{client_id}"
        )

        payload = json.dumps({"app_type": f"{app_type}"})
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": f"Bearer {settings.management_api_token}",
        }

        response = await make_request_with_error_handling(
            "PATCH", url, headers=headers, data=payload
        )

        return response.get("body")

    async def get_organizations_list(self, tenant):
        url = f"https://{tenant}.eu.auth0.com/api/v2/organizations"

        payload = {}
        headers = {
            "Accept": "application/json",
            "Authorization": f"Bearer {settings.management_api_token}",
        }

        response = await make_request_with_error_handling(
            "GET", url, headers=headers, data=payload
        )

        return response.get("body")

    async def remove_user_from_organization(self, user_id: str, organization_id: str):
        url = f"https://{settings.tenant_domain}.eu.auth0.com/api/v2/organizations/{organization_id}/members/{user_id}"

        payload = {}
        headers = {
            "Accept": "application/json",
            "Authorization": f"Bearer {settings.management_api_token}",
        }

        response = await make_request_with_error_handling(
            "GET", url, headers=headers, data=payload
        )

        return response.get("body")


organization_manager_obj = OrganizationManager()
