import pytest
from pathlib import Path
from adapters.chroma_adapter import ChromaVectorStore
from core.memory_store import MemoryStore

@pytest.fixture
def test_data_dir(tmp_path):
    """Create a temporary data directory for testing."""
    d = tmp_path / "data"
    d.mkdir()
    return d

@pytest.fixture
def mock_adapter(test_data_dir):
    """Isolated ChromaDB instance for testing."""
    return ChromaVectorStore(
        collection_name="test_collection",
        persist_dir=str(test_data_dir / "test_chroma")
    )

@pytest.fixture
def memory_store(mock_adapter):
    """MemoryStore instance with isolated adapter."""
    return MemoryStore(mock_adapter)

@pytest.fixture
def sample_memory():
    return {
        "memory_id": "T001",
        "date": "2024-01-01",
        "context": "Testing the memory store with a mock record.",
        "emotional_tone": "Neutral",
        "people": ["Tester"],
    }

@pytest.fixture
def seeded_db(mock_adapter, sample_memory):
    """DB pre-loaded with sample memories."""
    mock_adapter.upsert(
        sample_memory["memory_id"], 
        sample_memory["context"], 
        {k: v for k, v in sample_memory.items() if k != "context"}
    )
    return mock_adapter
