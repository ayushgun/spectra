import base64
from io import BytesIO
from pathlib import Path

from litestar import Litestar, get
from PIL import Image
from redis import Redis


class Object:
    def __init__(self, object_name: str) -> None:
        self.name = object_name

    def generate_caption() -> str:
        # TODO: Call Claude/OpenAI/Google API to generate image caption
        pass


class CameraFrame:
    def __init__(self, image_uri: str):
        self.image = self.decode_image_uri(image_uri)

    def decode_image_uri(self, base64_image_uri: str) -> Image.Image:
        encoded_data = base64_image_uri.split(",")[1]
        image_data = base64.b64decode(encoded_data)
        image = Image.open(BytesIO(image_data))
        return image

    def detect_objects(self) -> list[str]:
        pass

    def save_locally(self, file_name: Path) -> None:
        self.image.save(file_name)


@get("/")
async def index() -> str:
    return "API is available at 127.0.0.1:8000"


def main():
    r = Redis(host="localhost", port=6379, db=0)
    app = Litestar([index])


if __name__ == "__main__":
    main()
