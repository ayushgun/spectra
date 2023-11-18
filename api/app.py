import json
from pathlib import Path

import requests
from google.auth.transport.requests import Request
from google.oauth2 import service_account
from litestar import Litestar, get
from redis import Redis

import base64


class VisionClient:
    def __init__(self, gc_project_id: str, gc_service_account_key: Path) -> None:
        self.project_id = gc_project_id

        with open(gc_service_account_key, "r") as file:
            self.service_account_info = json.load(file)

    def refresh_access_token(self) -> str:
        credentials = service_account.Credentials.from_service_account_info(
            self.service_account_info,
            scopes=["https://www.googleapis.com/auth/cloud-platform"],
        )

        credentials.refresh(Request())
        return credentials.token

    def generate_description(self, b64_image_uri: str) -> str:
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


@get("/")
async def index() -> str:
    return "API is available at 127.0.0.1:8000"


def main():
    # r = Redis(host="localhost", port=6379, db=0)
    # app = Litestar([index])
    client = VisionClient("vision-405423", "gcloud_key.json")

    with open("city.jpg", "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
        print(client.generate_description(encoded_string.decode("utf-8")))


if __name__ == "__main__":
    main()
