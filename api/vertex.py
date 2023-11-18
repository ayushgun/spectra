import json
from pathlib import Path

import requests
from google.auth.transport.requests import Request
from google.oauth2 import service_account


class VisionClient:
    def __init__(self, gc_project_id: str, gc_service_account_key: Path) -> None:
        self.project_id = gc_project_id

        with open(gc_service_account_key, "r") as file:
            self.service_account_info = json.load(file)

    def refresh_access_token(self) -> str:
        """
        Refresh and return the Google Cloud API access token using the service account credentials.
        """

        credentials = service_account.Credentials.from_service_account_info(
            self.service_account_info,
            scopes=["https://www.googleapis.com/auth/cloud-platform"],
        )

        credentials.refresh(Request())
        return credentials.token

    def generate_description(self, b64_image_uri: str) -> str:
        """
        Send an image to Google Cloud Vision API and return the generated description of the image.
        """

        endpoint = (
            f"https://us-central1-aiplatform.googleapis.com/v1/projects/{self.project_id}"
            + "/locations/us-central1/publishers/google/models/imagetext:predict"
        )
        headers = {
            "Authorization": f"Bearer {self.refresh_access_token()}",
            "Content-Type": "application/json; charset=utf-8",
        }
        payload = {
            "instances": [{"image": {"bytesBase64Encoded": b64_image_uri}}],
            "parameters": {"sampleCount": 1, "language": "EN"},
        }

        response = requests.post(endpoint, headers=headers, json=payload)

        if response.status_code != 200:
            raise requests.exceptions.HTTPError(response.json())

        return response.json()["predictions"][0]
