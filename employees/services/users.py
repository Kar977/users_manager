import json

import aiohttp
from fastapi import HTTPException

from settings import Settings


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


user_manager_obj = UserManager()
