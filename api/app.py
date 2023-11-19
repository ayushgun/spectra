from litestar import Litestar, get, post
from functools import lru_cache

from llm import Eyesight, Tourguide

eyesight = Eyesight("vision-405423", "keys/service_account.json")
guide = Tourguide("keys/palm_key.json")


@lru_cache(maxsize=128)
def get_cached_description(uri: str) -> str:
    caption = eyesight.generate_description(uri)
    guidance = guide.rewrite_description(caption)
    return guidance


@get("/")
async def index() -> str:
    return "API is available at 127.0.0.1:8000"


@post("/snapshot/describe")
async def snapshot_description(data: dict[str, str]) -> dict[str, str]:
    guidance = get_cached_description(data["uri"])
    return {"response": guidance}


app = Litestar([index, snapshot_description])
