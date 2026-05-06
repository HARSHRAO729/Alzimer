from typing import Dict, Any, List

def validate_memory_record(record: Dict[str, Any]) -> bool:
    """Validate that a memory record has all required fields."""
    required_fields = ["memory_id", "date", "context", "emotional_tone"]
    for field in required_fields:
        if field not in record:
            return False
    return True

def sanitize_query(query: str) -> str:
    """Sanitize user query string."""
    if not query:
        return ""
    return query.strip()
