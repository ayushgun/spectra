from functools import lru_cache
from litestar import Litestar, get, post, Response
from ai import Snapshot, Tourguide

Snapshot.gc_project_id = "vision-405423"
Snapshot.gc_service_key_file = "keys/service_account.json"
guide = Tourguide("keys/palm_key.json")


@lru_cache(maxsize=128)
def get_cached_description(uri: str) -> str:
    image_frame = Snapshot(uri)

    if image_frame.has_hazard():
        return Response(
            status_code=200,
            content={"response": guide.generate_contextual_description(image_frame)},
        )

    return Response(status_code=204, content=None)


@get("/")
async def index() -> str:
    return "API is available at 127.0.0.1:8000"


@post("/snapshot/describe")
async def snapshot_description(data: dict[str, str]) -> dict[str, str]:
    return get_cached_description(data["uri"])


app = Litestar([index, snapshot_description])
