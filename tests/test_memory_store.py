import pytest
from core.memory_store import MemoryStore
from pathlib import Path
import json

def test_add_and_count_memory(memory_store, sample_memory):
    assert memory_store.count() == 0
    memory_store.add_memory(sample_memory)
    assert memory_store.count() == 1

def test_get_all_memories(memory_store, sample_memory):
    memory_store.add_memory(sample_memory)
    memories = memory_store.get_all_memories()
    assert len(memories) == 1
    assert memories[0]["memory_id"] == "T001"
    assert memories[0]["context"] == sample_memory["context"]

def test_delete_memory(memory_store, sample_memory):
    memory_store.add_memory(sample_memory)
    assert memory_store.count() == 1
    memory_store.delete_memory("T001")
    assert memory_store.count() == 0

def test_load_seed_data(memory_store, test_data_dir):
    # Create a dummy JSON file
    memories = [
        {
            "memory_id": "S001",
            "date": "2024-02-01",
            "context": "Seed memory 1",
            "emotional_tone": "Happy"
        },
        {
            "memory_id": "S002",
            "date": "2024-02-02",
            "context": "Seed memory 2",
            "emotional_tone": "Calm"
        }
    ]
    seed_file = test_data_dir / "test_memories.json"
    with open(seed_file, "w") as f:
        json.dump(memories, f)
    
    count = memory_store.load_seed_data(str(seed_file))
    assert count == 2
    assert memory_store.count() == 2

def test_invalid_memory_record(memory_store):
    invalid_record = {"memory_id": "I001"} # Missing required fields
    with pytest.raises(ValueError, match="Invalid memory record"):
        memory_store.add_memory(invalid_record)
