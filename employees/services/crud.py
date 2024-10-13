import json
import os

import requests
from dotenv import load_dotenv

load_dotenv()


class OrganizationManager:

    def create_organization(self, name: str, display_name: str, primary_color: str =  '#eb4034', background_color: str = '#e0b9b6'):

        url = f"https://{os.getenv('TENANT_DOMAIN')}.eu.auth0.com/api/v2/organizations"

        payload = json.dumps({
            "name": f"{name}",
            "display_name": f"{display_name}",
            "branding": {
                "colors": {
                    "primary": f"{primary_color}",
                    "page_background": f"{background_color}"
                }
            },
            "metadata": {},
            "enabled_connections": [
                {
                    "connection_id": f"{os.getenv('DATABASE_ID_CONNECTION')}",
                    "assign_membership_on_login": True,
                    "show_as_button": True,
                    "is_signup_enabled": True
                }
            ]
        })
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Authorization': f"Bearer {os.getenv('MANAGEMENT_API_TOKEN')}"
        }

        response = requests.request("POST", url, headers=headers, data=payload)

        return response.text

    def get_organization_by_name(self, name: str = 'nowy-polski-salon'):

        url = f"https://{os.getenv('TENANT_DOMAIN')}.eu.auth0.com/api/v2/organizations/name/{name}"

        payload = {}
        headers = {
            'Accept': 'application/json',
            'Authorization': f"Bearer {os.getenv('MANAGEMENT_API_TOKEN')}"
        }

        response = requests.request("GET", url, headers=headers, data=payload)

        return response.text

    def delete_organization_by_identifier(self, identifier: str):

        url = f"https://{os.getenv('TENANT_DOMAIN')}.eu.auth0.com/api/v2/organizations/{identifier}"

        payload = {}
        headers = {
            'Authorization': f"Bearer {os.getenv('MANAGEMENT_API_TOKEN')}"
        }

        response = requests.request("DELETE", url, headers=headers, data=payload)

        return response.text

    def modify_organization(self, identifier: str, name: str = None, display_name: str = None, logo_url: str = None, primary_color: str = None,
                            background_color: str = None):

        url = f"https://{os.getenv('TENANT_DOMAIN')}.eu.auth0.com/api/v2/organizations/{identifier}"

        payload = {}

        if name:
            payload["name"] = name
        if display_name:
            payload["display_name"] = display_name
        if logo_url or primary_color or background_color:
            payload["branding"] = {}
            if logo_url:
                payload["branding"]["logo_url"] = logo_url
            if primary_color or background_color:
                payload["branding"]["colors"] = {}
                if primary_color:
                    payload["branding"]["colors"]["primary"] = primary_color
                if background_color:
                    payload["branding"]["colors"]["page_background"] = background_color

        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Authorization': f"Bearer {os.getenv('MANAGEMENT_API_TOKEN')}"
        }

        response = requests.request("PATCH", url, headers=headers, data=json.dumps(payload))

        if response.status_code == 200:
            print("Organization updated successfully")
        else:
            print("Failed to updated organization")
        return response.text


organization_manager_obj = OrganizationManager()