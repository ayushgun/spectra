from litestar import Litestar, get, post
from redis import Redis

from llm import Eyesight, Tourguide

eyesight = Eyesight("vision-405423", "keys/service_account.json")
guide = Tourguide("keys/palm_key.json")

redis = Redis(host="localhost", port=6379, db=0)


@get("/")
async def index() -> str:
    return "API is available at 127.0.0.1:8000"


@post("/snapshot/describe")
async def snapshot_description(data: dict[str, str]) -> dict[str, str]:
    caption = eyesight.generate_description(data["uri"])
    guidance = guide.rewrite_description(caption)
    return {"response": guidance}


app = Litestar([index, snapshot_description])
