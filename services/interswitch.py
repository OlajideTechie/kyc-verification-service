import logging
import requests
from django.conf import settings

logger = logging.getLogger(__name__)


class InterswitchClient:

    def __init__(self):
        self.auth_url = settings.INTERSWITCH_AUTH_URL
        self.verify_passport_url = settings.INTERSWITCH_VERIFY_PASSPORT_URL
        self.client_id = settings.INTERSWITCH_CLIENT_ID
        self.client_secret = settings.INTERSWITCH_CLIENT_SECRET
        self.timeout = 15

    def authenticate(self) -> str:
        """
        Fetch OAuth token from Interswitch
        """

        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
        }

        data = {
            "grant_type": "client_credentials",
            "scope": "profile",
        }

        try:
            response = requests.post(
                self.auth_url,
                headers=headers,
                data=data,
                auth=(self.client_id, self.client_secret),
                timeout=self.timeout,
            )

            response.raise_for_status()

            token = response.json().get("access_token")

            if not token:
                raise ValueError("No access_token returned from Interswitch")

            return token

        except requests.exceptions.RequestException as exc:
            logger.exception("Interswitch authentication failed")
            raise RuntimeError("Failed to authenticate with Interswitch") from exc

    def verify_passport(self, token: str, payload: dict) -> dict:
        """
        Verify passport details using Interswitch API
        """

        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "Accept": "application/json",
        }

        try:
            logger.info(f"Sending passport verification payload: {payload}")

            response = requests.post(
                self.verify_passport_url,
                headers=headers,
                json=payload,
                timeout=self.timeout,
            )

            if response.status_code >= 400:
                logger.error(
                    f"Interswitch verification failed | "
                    f"Status: {response.status_code} | "
                    f"Response: {response.text}"
                )

                return {
                    "status": "error",
                    "status_code": response.status_code,
                    "provider_response": response.json() if response.text else None,
                }

            return response.json()

        except requests.exceptions.Timeout:
            logger.exception("Interswitch verification timeout")
            return {"status": "error", "message": "Verification request timed out"}

        except requests.exceptions.RequestException as exc:
            logger.exception("Interswitch verification request failed")
            return {"status": "error", "message": str(exc)}