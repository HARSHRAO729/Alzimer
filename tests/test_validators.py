from utils.validators import validate_memory_record
import pytest

def test_validate_memory_record_valid():
    valid_record = {
        "memory_id": "mem_123",
        "date": "2024-05-01",
        "context": "Something happened.",
        "emotional_tone": "Happy",
        "people": ["Alice"]
    }
    assert validate_memory_record(valid_record) == True

def test_validate_memory_record_missing_fields():
    invalid_record = {
        "memory_id": "mem_123",
        # "date" missing
        "context": "Something happened."
    }
    assert validate_memory_record(invalid_record) == False

def test_validate_memory_record_wrong_types():
    invalid_record = {
        "memory_id": 123, # Should be string
        "date": "2024-05-01",
        "context": "Something happened.",
        "emotional_tone": "Happy",
        "people": "Alice" # Should be list
    }
    assert validate_memory_record(invalid_record) == False
