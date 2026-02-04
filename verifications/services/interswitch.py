import requests
from django.conf import settings


class InterswitchClient:
    def __init__(self):
        self.auth_url = settings.INTERSWITCH_AUTH_URL
        self.verify_passport_url = settings.INTERSWITCH_VERIFY_PASSPORT_URL
        self.client_id = settings.INTERSWITCH_CLIENT_ID
        self.client_secret = settings.INTERSWITCH_CLIENT_SECRET

    def authenticate(self) -> str:
        """
        Calls Interswitch auth endpoint and returns access token
        """
        url = settings.INTERSWITCH_AUTH_URL

        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
        }

        data = {
            "grant_type": "client_credentials",
            "scope": "profile"
            }
        
        response = requests.post(
            url,
            data=data,
            auth=(
                settings.INTERSWITCH_CLIENT_ID,
                settings.INTERSWITCH_CLIENT_SECRET
            ),
            timeout=15 # seconds for the request to complete
        )
        response.raise_for_status()
        return response.json().get("access_token")



    def verify_passport(self, token: str, payload: dict) -> dict:
        """
        Verifies passport details
        """
        url = settings.INTERSWITCH_VERIFY_PASSPORT_URL

        response = requests.post(
            url,
            headers={
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json",
                "Accept": "application/json",
            },
            json=payload,
            timeout=15,
        )

        response.raise_for_status()
        return response.json()
