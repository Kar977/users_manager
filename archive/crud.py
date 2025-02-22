"""
import json
import logging

import aiohttp
from fastapi import HTTPException

from settings import Settings

logger = logging.getLogger(__name__)


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

        url = f"https://{Settings.TENANT_DOMAIN}.eu.auth0.com/api/v2/organizations"

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
                        "connection_id": f"{Settings.DATABASE_ID_CONNECTION}",
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
            "Authorization": f"Bearer {Settings.MANAGEMENT_API_TOKEN}",
        }

        response = await make_request_with_error_handling(
            "POST", url, headers=headers, data=payload
        )

        return response.get("body")

    async def get_organization_by_name(self, name: str = "nowy-polski-salon"):

        url = f"https://{Settings.TENANT_DOMAIN}.eu.auth0.com/api/v2/organizations/name/{name}"

        payload = {}
        headers = {
            "Accept": "application/json",
            "Authorization": f"Bearer {Settings.MANAGEMENT_API_TOKEN}",
        }

        response = await make_request_with_error_handling(
            "GET", url, headers=headers, data=payload
        )
        return response.get("body")

    async def delete_organization_by_identifier(self, identifier: str):

        url = f"https://{Settings.TENANT_DOMAIN}.eu.auth0.com/api/v2/organizations/{identifier}"

        payload = {}
        headers = {"Authorization": f"Bearer {Settings.MANAGEMENT_API_TOKEN}"}

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

        url = f"https://{Settings.TENANT_DOMAIN}.eu.auth0.com/api/v2/organizations/{identifier}"

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
            "Authorization": f"Bearer {Settings.MANAGEMENT_API_TOKEN}",
        }

        response = await make_request_with_error_handling(
            "PATCH", url, headers=headers, data=json.dumps(payload)
        )
        return response.get("body")

    async def change_client_type(self, client_id: str, app_type: str):
        url = (
            f"https://{Settings.TENANT_DOMAIN}.eu.auth0.com/api/v2/clients/{client_id}"
        )

        payload = json.dumps({"app_type": f"{app_type}"})
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": f"Bearer {Settings.MANAGEMENT_API_TOKEN}",
        }

        response = await make_request_with_error_handling(
            "PATCH", url, headers=headers, data=payload
        )

        return response.get("body")


class UserManager:

    async def create_user(self, email: str, name: str, family_name: str, username: str):

        url = f"https://{Settings.TENANT_DOMAIN}.eu.auth0.com/api/v2/users"

        payload = json.dumps(
            {
                "email": f"{email}",
                "user_metadata": {},
                "email_verified": False,
                "app_metadata": {},
                "family_name": f"{family_name}",
                "name": f"{name}",
                "connection": "Username-Password-Authentication",
                "verify_email": True,
                "username": f"{username}",
                "password": "k1#M088sBM",  # ToDo change on some random
            }
        )
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": f"Bearer {Settings.MANAGEMENT_API_TOKEN}",
        }

        response = await make_request_with_error_handling(
            "POST", url, headers=headers, data=payload
        )

        await self.send_email_with_password_change(email)

        return response.get("body")

    async def list_users(self):

        url = f"https://{Settings.TENANT_DOMAIN}.eu.auth0.com/api/v2/users"

        payload = {}
        headers = {
            "Accept": "application/json",
            "Authorization": f"Bearer {Settings.MANAGEMENT_API_TOKEN}",
        }

        response = await make_request_with_error_handling(
            "GET", url, headers=headers, data=payload
        )

        return response.get("body")

    async def get_user_id_by_email(self, email: str):
        payload = {}
        headers = {
            "content-type": "application/json",
            "authorization": f"Bearer {Settings.MANAGEMENT_API_TOKEN}",
        }

        response = await make_request_with_error_handling(
            "GET",
            f"https://{Settings.TENANT_DOMAIN}.eu.auth0.com/api/v2/users-by-email?email={email}",
            headers=headers,
            data=payload,
        )

        received_payload = json.loads(response.get("body"))

        try:
            user_id = received_payload[0]["identities"][0]["user_id"]
        except IndexError as exc:
            raise HTTPException(
                status_code=404,
                detail=f"User not found and system raise IndexError = {exc}",
            )
        return str(user_id)

    async def send_email_with_password_change(self, email: str):

        payload = {
            "email": f"{email}",
            "connection": "Username-Password-Authentication",
        }

        payload = json.dumps(payload)
        headers = {
            "content-type": "application/json",
            "Authorization": f"Bearer {Settings.MANAGEMENT_API_TOKEN}",
        }

        response = await make_request_with_error_handling(
            "POST",
            f"https://{Settings.TENANT_DOMAIN}.eu.auth0.com/dbconnections/change_password",
            data=payload,
            headers=headers,
        )

        return response.get("body")

    async def delete_user(self, email: str):

        user_id = await user_manager_obj.get_user_id_by_email(email=email)

        url = f"https://{Settings.TENANT_DOMAIN}.eu.auth0.com/api/v2/users/auth0|{user_id}"

        payload = {}
        headers = {"Authorization": f"Bearer {Settings.MANAGEMENT_API_TOKEN}"}

        response = await make_request_with_error_handling(
            "DELETE", url, headers=headers, data=payload
        )

        return response.get("body")

    async def modify_user(
        self,
        user_id: str,
        blocked: bool = None,
        email_verified: bool = None,
        email: str = None,
        phone_number: str = None,
        phone_verified: bool = None,
        user_metadata: dict = None,
        app_metadata: dict = None,
        given_name: str = None,
        family_name: str = None,
        name: str = None,
        nickname: str = None,
        picture: str = None,
        verify_email: bool = None,
        verify_phone_number: bool = None,
        password: str = None,
        connection: str = None,
        client_id: str = None,
        username: str = None,
    ):

        url = f"https://{Settings.TENANT_DOMAIN}.eu.auth0.com/api/v2/users/auth0|{user_id}"

        payload = {
            "blocked": blocked,
            "email_verified": email_verified,
            "email": email,
            "phone_number": phone_number,
            "phone_verified": phone_verified,
            "user_metadata": user_metadata,
            "app_metadata": app_metadata,
            "given_name": given_name,
            "family_name": family_name,
            "name": name,
            "nickname": nickname,
            "picture": picture,
            "verify_email": verify_email,
            "verify_phone_number": verify_phone_number,
            "password": password,
            "connection": connection,
            "client_id": client_id,
            "username": username,
        }

        payload = json.dumps({k: v for k, v in payload.items() if v is not None})

        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": f"Bearer {Settings.MANAGEMENT_API_TOKEN}",
        }

        response = await make_request_with_error_handling(
            "PATCH", url, headers=headers, data=payload
        )

        return response.get("body")

    async def invite_user_to_organization(self, user_email: str):

        url = f"https://{Settings.TENANT_DOMAIN}.eu.auth0.com/api/v2/organizations/{Settings.ORGANIZATION_IDENTIFIER}/invitations"

        payload = json.dumps(
            {
                "inviter": {"name": "Brodacz TEAM"},
                "invitee": {"email": f"{user_email}"},
                "client_id": f"{Settings.CLIENT_ID}",
                "connection_id": f"{Settings.DATABASE_ID_CONNECTION}",
                "app_metadata": {},
                "user_metadata": {},
                "ttl_sec": 0,
                # "roles": [ #ToDo implement the roles
                #    "string"
                # ],
                "send_invitation_email": True,
            }
        )
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": f"Bearer {Settings.MANAGEMENT_API_TOKEN}",
        }

        response = await make_request_with_error_handling(
            "POST", url, headers=headers, data=payload
        )

        return response.get("body")


organization_manager_obj = OrganizationManager()
user_manager_obj = UserManager()

"""
