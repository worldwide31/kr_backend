from datetime import UTC, datetime
from typing import Any

from bson import ObjectId

from app.db.mongo import get_mongo_db


def stringify_event(document: dict[str, Any]) -> dict[str, str]:
    return {
        "id": str(document.get("_id")),
        "action": str(document.get("action")),
        "entity_type": str(document.get("entity_type")),
        "entity_id": str(document.get("entity_id")),
        "message": str(document.get("message")),
        "created_at": document.get("created_at", datetime.now(UTC)).isoformat(),
    }


async def write_event(action: str, entity_type: str, entity_id: int | str, message: str) -> None:
    db = get_mongo_db()
    await db.audit_events.insert_one(
        {
            "action": action,
            "entity_type": entity_type,
            "entity_id": str(entity_id),
            "message": message,
            "created_at": datetime.now(UTC),
        }
    )


async def list_events(limit: int = 20) -> list[dict[str, str]]:
    db = get_mongo_db()
    cursor = db.audit_events.find().sort("created_at", -1).limit(limit)
    return [stringify_event(item) async for item in cursor]


async def get_event(event_id: str) -> dict[str, Any] | None:
    db = get_mongo_db()
    document = await db.audit_events.find_one({"_id": ObjectId(event_id)})
    return stringify_event(document) if document else None

