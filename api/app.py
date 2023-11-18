from litestar import Litestar, get, post
from redis import Redis

from vertex import VisionClient

vision = VisionClient("vision-405423", "gcloud_key.json")
redis = Redis(host="localhost", port=6379, db=0)


@get("/")
async def index() -> str:
    return "API is available at 127.0.0.1:8000"


@post("/snapshot/describe")
async def snapshot_description(data: dict[str, str]) -> str:
    caption = vision.generate_description(data["uri"])

    # Generate nuanced caption using base caption

    return caption


app = Litestar([index, snapshot_description])
