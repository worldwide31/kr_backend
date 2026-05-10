from datetime import datetime


def make_number(prefix: str, entity_id: int) -> str:
    return f"{prefix}-{datetime.now().strftime('%Y%m%d')}-{entity_id:05d}"

