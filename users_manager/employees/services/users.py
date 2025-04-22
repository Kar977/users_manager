import json
import secrets

import aiohttp
from fastapi import HTTPException
from users_manager.settings import settings


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


class UserManager:

    async def create_user(self, email: str, name: str, family_name: str, username: str):

        url = f"https://{settings.tenant_domain}.eu.auth0.com/api/v2/users"
        new_password = secrets.token_urlsafe(8)
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
                "password": new_password,
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

        await self.send_email_with_password_change(email)

        return response.get("body")

    async def list_users(self):
        url = f"https://{settings.tenant_domain}.eu.auth0.com/api/v2/users"

        payload = {}
        headers = {
            "Accept": "application/json",
            "Authorization": f"Bearer {settings.management_api_token}",
        }

        response = await make_request_with_error_handling(
            "GET", url, headers=headers, data=payload
        )

        return response.get("body")

    async def get_user_id_by_email(self, email: str):
        payload = {}
        headers = {
            "content-type": "application/json",
            "authorization": f"Bearer {settings.management_api_token}",
        }

        response = await make_request_with_error_handling(
            "GET",
            f"https://{settings.tenant_domain}.eu.auth0.com/api/v2/users-by-email?email={email}",
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
            "Authorization": f"Bearer {settings.management_api_token}",
        }

        response = await make_request_with_error_handling(
            "POST",
            f"https://{settings.tenant_domain}.eu.auth0.com/dbconnections/change_password",
            data=payload,
            headers=headers,
        )

        return response.get("body")

    async def delete_user(self, email: str):

        user_id = await user_manager_obj.get_user_id_by_email(email=email)

        url = f"https://{settings.tenant_domain}.eu.auth0.com/api/v2/users/auth0|{user_id}"

        payload = {}
        headers = {"Authorization": f"Bearer {settings.management_api_token}"}

        response = await make_request_with_error_handling(
            "DELETE", url, headers=headers, data=payload
        )

        return response.get("body")

    async def modify_user(self, **kwargs):

        url = f"https://{settings.tenant_domain}.eu.auth0.com/api/v2/users/auth0|{kwargs.get('user_id')}"

        payload = {
            "given_name": kwargs.get("given_name", None),
            "family_name": kwargs.get("family_name", None),
            "name": kwargs.get("name", None),
            "nickname": kwargs.get("nickname", None),
            "picture": kwargs.get("picture", None),
            "verify_email": kwargs.get("verify_email", None),
            "verify_phone_number": kwargs.get("verify_phone_number", None),
            "password": kwargs.get("password", None),
            "username": kwargs.get("username", None),
        }

        payload = json.dumps({k: v for k, v in payload.items() if v is not None})

        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": f"Bearer {settings.management_api_token}",
        }

        response = await make_request_with_error_handling(
            "PATCH", url, headers=headers, data=payload
        )

        return response.get("body")

    async def invite_user_to_organization(
        self,
        user_email: str,
        organization_id: str,
    ):

        url = f"https://{settings.tenant_domain}.eu.auth0.com/api/v2/organizations/{organization_id}/invitations"

        payload = json.dumps(
            {
                "inviter": {"name": "Brodacz TEAM"},
                "invitee": {"email": f"{user_email}"},
                "client_id": f"{settings.client_id}",
                "connection_id": f"{settings.database_id_connection}",
                "app_metadata": {},
                "user_metadata": {},
                "ttl_sec": 0,
                "roles": ["employee"],
                "send_invitation_email": True,
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

    async def add_roles_to_already_exsisting_user_in_organization(
        self, user_id: str, organization_id: str, roles: list
    ):

        url = f"https://{settings.tenant_domain}.eu.auth0.com/api/v2/organizations/{organization_id}/members/{user_id}/roles"

        payload = json.dumps({"roles": roles})
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {settings.management_api_token}",
        }

        response = await make_request_with_error_handling(
            "POST", url, headers=headers, data=payload
        )

        return response.get("body")


user_manager_obj = UserManager()
