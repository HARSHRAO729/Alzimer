import pytest
from core.repository import MemoryRepository
from adapters.chroma_adapter import ChromaVectorStore
import os
import shutil

@pytest.fixture
def repo(tmp_path):
    # Setup a fresh test DB in a temp directory
    test_db_dir = tmp_path / "test_repo_db"
    
    adapter = ChromaVectorStore(collection_name="test_repo", persist_dir=str(test_db_dir))
    repository = MemoryRepository(adapter)
    yield repository

def test_repository_lifecycle(repo):
    # 1. Test add_memory
    mem = {
        "memory_id": "test_1",
        "date": "2024-05-01 10:00 AM",
        "context": "The keys are on the kitchen counter.",
        "emotional_tone": "Neutral",
        "people": ["User"]
    }
    repo.add_memory(mem)
    assert repo.count() == 1
    
    # 2. Test get_history
    history = repo.get_history()
    assert len(history) == 1
    assert history[0]["context"] == "The keys are on the kitchen counter."
    
    # 3. Test get_related_memories
    related = repo.get_related_memories("where are the keys?")
    assert len(related) > 0
    assert "keys" in related[0]["text"].lower()

def test_repository_reseed(repo, tmp_path):
    # Create a temporary memories.json for testing
    test_json = tmp_path / "memories.json"
    import json
    data = [
        {
            "memory_id": "seed_1",
            "date": "2024-05-01 10:00 AM",
            "context": "Seed memory context.",
            "emotional_tone": "Neutral",
            "people": ["System"]
        }
    ]
    with open(test_json, "w") as f:
        json.dump(data, f)
        
    count = repo.store.load_seed_data(json_path=str(test_json))
    assert count == 1
    assert repo.count() == 1

def test_assistant_query_mocked(repo, mocker):
    # Mock the generate_response generator
    mocker.patch('core.repository.generate_response', return_value=iter(["This is ", "a test response"]))
    
    response_gen = repo.query_assistant("Hello")
    full_response = "".join(list(response_gen))
    
    assert full_response == "This is a test response"
