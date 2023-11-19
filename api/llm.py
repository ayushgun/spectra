import json
from pathlib import Path

import google.generativeai as palm
import requests
from google.auth.transport.requests import Request
from google.oauth2 import service_account


class Tourguide:
    def __init__(self, palm_api_key_file: str) -> None:
        with open(palm_api_key_file, "r") as file:
            key_file = json.load(file)
            palm.configure(api_key=key_file["api_key"])

    def fill_template_prompt(self, description: str) -> str:
        return f"""
        Given a simple scene description: "{description}"

        In only two sentences, return a description as if you were guiding a walking blind person,
        noting anything they may need to consider for their safety and navigation. Do not make any
        assumptions beyond the initial description provided to you. For example, do not make comments
        on the sounds of the scene. Only respond with the new description, nothing else. Always answer
        in English.

        Think step by step. Consider my question carefully and think of the academic or professional
        expertise of someone that could best answer my question. You have the experience of someone
        with expert knowledge in that area. Be helpful and answer in detail while preferring to use
        nformation from reputable sources.
        """

    def rewrite_description(self, basic_description: str) -> str:
        prompt = self.fill_template_prompt(basic_description)
        response = palm.chat(messages=[prompt])
        return f"{'. '.join(response.last.split('. ')[:2])}."


class Eyesight:
    def __init__(self, gc_project_id: str, gc_service_key_file: Path) -> None:
        self.project_id = gc_project_id

        with open(gc_service_key_file, "r") as file:
            self.service_account_info = json.load(file)

    def refresh_access_token(self) -> str:
        """
        Refresh and return the Google Cloud API access token using the account credentials.
        """

        credentials = service_account.Credentials.from_service_account_info(
            self.service_account_info,
            scopes=["https://www.googleapis.com/auth/cloud-platform"],
        )

        credentials.refresh(Request())
        return credentials.token

    def generate_description(self, image_uri: str) -> str:
        """
        Send an image URI to Google Cloud Vision API and return the generated description.
        """

        base64_string = image_uri.split(",")[1] if "," in image_uri else image_uri

        endpoint = (
            f"https://us-central1-aiplatform.googleapis.com/v1/projects/{self.project_id}"
            + "/locations/us-central1/publishers/google/models/imagetext:predict"
        )
        headers = {
            "Authorization": f"Bearer {self.refresh_access_token()}",
            "Content-Type": "application/json; charset=utf-8",
        }
        payload = {
            "instances": [{"image": {"bytesBase64Encoded": base64_string}}],
            "parameters": {"sampleCount": 1, "language": "EN"},
        }

        response = requests.post(endpoint, headers=headers, json=payload)

        if response.status_code != 200:
            raise requests.exceptions.HTTPError(response.json())

        return response.json()["predictions"][0]
