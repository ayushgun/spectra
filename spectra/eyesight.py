import json
from pathlib import Path

import google.generativeai as palm
import requests
from google.auth.transport.requests import Request
from google.oauth2 import service_account


class Snapshot:
    gc_project_id: str = None
    gc_service_key_file: Path = None

    def __init__(self, image_uri: str) -> None:
        self.image_uri = image_uri
        self.base64_uri = self.to_base64_uri()

        with open(Snapshot.gc_service_key_file, "r") as file:
            self.service_account_info: dict[str, str] = json.load(file)

    def to_base64_uri(self) -> str:
        """
        Converts the image URI to a Base64 encoded URI.
        """

        return self.image_uri.split(",")[1] if "," in self.image_uri else self.image_uri

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

    def has_hazard(self) -> bool:
        """
        Determines whether the image associated with the Snapshot instance contains any hazards.
        """

        endpoint = (
            f"https://us-central1-aiplatform.googleapis.com/v1/projects/{Snapshot.gc_project_id}"
            + "/locations/us-central1/publishers/google/models/imagetext:predict"
        )
        prompt = (
            "Is there anything potentially dangerous in this image? "
            + "Reply only with 'yes' or 'no'"
        )
        headers = {
            "Authorization": f"Bearer {self.refresh_access_token()}",
            "Content-Type": "application/json; charset=utf-8",
        }
        payload = {
            "instances": [
                {"prompt": prompt, "image": {"bytesBase64Encoded": self.base64_uri}}
            ],
            "parameters": {"sampleCount": 1, "language": "EN"},
        }

        response = requests.post(endpoint, headers=headers, json=payload)

        if response.status_code != 200:
            raise requests.exceptions.HTTPError(response.json())

        return response.json()["predictions"][0] == "yes"

    def generate_description(self) -> str:
        """
        Send an image URI to Google Cloud Vision API and return the generated description.
        """

        endpoint = (
            f"https://us-central1-aiplatform.googleapis.com/v1/projects/{Snapshot.gc_project_id}"
            + "/locations/us-central1/publishers/google/models/imagetext:predict"
        )
        headers = {
            "Authorization": f"Bearer {self.refresh_access_token()}",
            "Content-Type": "application/json; charset=utf-8",
        }
        payload = {
            "instances": [{"image": {"bytesBase64Encoded": self.base64_uri}}],
            "parameters": {"sampleCount": 1, "language": "EN"},
        }

        response = requests.post(endpoint, headers=headers, json=payload)

        if response.status_code != 200:
            raise requests.exceptions.HTTPError(response.json())

        return response.json()["predictions"][0]


class Tourguide:
    def __init__(self, palm_api_key_file: Path) -> None:
        with open(palm_api_key_file, "r") as file:
            key_file = json.load(file)
            palm.configure(api_key=key_file["api_key"])

    def fill_template_prompt(self, description: str) -> str:
        """
        Creates a structured prompt for the PALM API, given a simple scene description, tailored
        for assisting a walking blind person.
        """

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

    def generate_contextual_description(self, frame: Snapshot) -> str:
        """
        Generates a contextually relevant description, focusing on a blind person's safety.
        """

        prompt = self.fill_template_prompt(frame.generate_description())
        response = palm.chat(messages=[prompt])

        if not response:
            raise RuntimeError("Unable to generate contex-aware description")

        return f"{'. '.join(response.last.split('. ')[:2])}."
