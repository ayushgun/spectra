import base64
import json
from enum import Enum, auto
from pathlib import Path

import requests
from google.auth.transport.requests import Request
from google.oauth2 import service_account


class VoiceGender(Enum):
    MALE = auto()
    FEMALE = auto()


class TTSMessage:
    gc_project_id: str = None
    gc_service_key_file: Path = None

    def __init__(self, text: str) -> None:
        self.text = text

        with open(TTSMessage.gc_service_key_file, "r") as file:
            self.service_account_info: dict[str, str] = json.load(file)

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

    def save_b64_as_mp3(self, b64_audio, filename: str) -> None:
        audio_data = base64.b64decode(b64_audio)

        # Write the decoded data to an MP3 file
        with open(filename, "wb") as audio_file:
            audio_file.write(audio_data)

    def to_audio(self, filename: str, gender: VoiceGender) -> None:
        endpoint = "https://texttospeech.googleapis.com/v1/text:synthesize"
        headers = {
            "Authorization": f"Bearer {self.refresh_access_token()}",
            "Content-Type": "application/json; charset=utf-8",
        }
        payload = {
            "input": {"text": self.text},
            "voice": {
                "languageCode": "en-US",
                "name": "en-US-Studio-" + ("M" if gender == VoiceGender.MALE else "O"),
            },
            "audioConfig": {"audioEncoding": "MP3", "speakingRate": 1.4},
        }

        response = requests.post(endpoint, headers=headers, json=payload)

        if response.status_code != 200:
            raise requests.exceptions.HTTPError(response.json())

        self.save_b64_as_mp3(response.json()["audioContent"], filename)
