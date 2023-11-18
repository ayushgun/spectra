from litestar import Litestar, get
from redis import Redis

from vertex import VisionClient


vision = VisionClient("vision-405423", "gcloud_key.json")
redis = Redis(host="localhost", port=6379, db=0)


@get("/")
async def index() -> str:
    return "API is available at 127.0.0.1:8000"


@get("/snapshot/describe")
async def snapshot_description(b64_snapshot_uri) -> str:
    caption = vision.generate_description(b64_snapshot_uri)

    # TODO: generate nuanced LLM message


app = Litestar([index])
