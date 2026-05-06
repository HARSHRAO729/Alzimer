from typing import Dict, Any, List

def validate_memory_record(record: Dict[str, Any]) -> bool:
    """Validate that a memory record has all required fields and correct types."""
    required_fields = {
        "memory_id": str,
        "date": str,
        "context": str,
        "emotional_tone": str
    }
    for field, field_type in required_fields.items():
        if field not in record:
            return False
        if not isinstance(record[field], field_type):
            return False
            
    if "people" in record and not isinstance(record["people"], list):
        return False
        
    return True

def sanitize_query(query: str) -> str:
    """Sanitize user query string."""
    if not query:
        return ""
    return query.strip()
