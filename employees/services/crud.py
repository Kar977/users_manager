import json

import requests

from settings import Settings


def make_request_with_error_handling(method: str, url: str, headers=None, data=None):

    try:
        response = requests.request(method, url, headers=headers, data=data)
        response.status_code
        return response.text
    except requests.exceptions.HTTPError as http_err:
        return f"HTTP Error: {http_err}"
    except requests.exceptions.RequestException as req_err:
        return f"HTTP error occurred: {req_err}"
    except Exception as err:
        return f"An error occurred: {err}"


class OrganizationManager:

    def create_organization(
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

        response = make_request_with_error_handling(
            "POST", url, headers=headers, data=payload
        )
        return response

    def get_organization_by_name(self, name: str = "nowy-polski-salon"):

        url = f"https://{Settings.TENANT_DOMAIN}.eu.auth0.com/api/v2/organizations/name/{name}"

        payload = {}
        headers = {
            "Accept": "application/json",
            "Authorization": f"Bearer {Settings.MANAGEMENT_API_TOKEN}",
        }

        response = make_request_with_error_handling(
            "GET", url, headers=headers, data=payload
        )
        return response

    def delete_organization_by_identifier(self, identifier: str):

        url = f"https://{Settings.TENANT_DOMAIN}.eu.auth0.com/api/v2/organizations/{identifier}"

        payload = {}
        headers = {"Authorization": f"Bearer {Settings.MANAGEMENT_API_TOKEN}"}

        response = make_request_with_error_handling(
            "DELETE", url, headers=headers, data=payload
        )
        return response.text

    def modify_organization(
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

        response = make_request_with_error_handling(
            "PATCH", url, headers=headers, data=json.dumps(payload)
        )
        return response


organization_manager_obj = OrganizationManager()
