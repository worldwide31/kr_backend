from fastapi import APIRouter, Query

from app.schemas.dashboard import ActivityEvent
from app.services.audit import list_events

router = APIRouter(prefix="/events", tags=["events"])


@router.get("", response_model=list[ActivityEvent])
async def read_events(limit: int = Query(default=20, ge=1, le=100)) -> list[dict[str, str]]:
    return await list_events(limit=limit)

