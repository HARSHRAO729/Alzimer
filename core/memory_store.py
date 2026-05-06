from typing import List, Dict, Any
from adapters.base import VectorStoreAdapter
from utils.file_io import load_json
from utils.validators import validate_memory_record
import config

class MemoryStore:
    """High-level store for managing memory records."""
    
    def __init__(self, adapter: VectorStoreAdapter):
        self.adapter = adapter
    
    def load_seed_data(self, json_path: str = str(config.MEMORIES_JSON)) -> int:
        """Load memories from a JSON file into the vector store."""
        memories = load_json(json_path)
        count = 0
        for mem in memories:
            if validate_memory_record(mem):
                self.add_memory(mem)
                count += 1
        return count
    
    def add_memory(self, record: Dict[str, Any]) -> None:
        """Add a single memory record to the store."""
        if not validate_memory_record(record):
            raise ValueError("Invalid memory record")
        
        # We use the 'context' field for embedding, everything else is metadata
        self.adapter.upsert(
            id=record["memory_id"],
            text=record["context"],
            metadata={k: v for k, v in record.items() if k != "context"}
        )
    
    def get_all_memories(self) -> List[Dict[str, Any]]:
        """Return all memories in the store."""
        results = self.adapter.list_all()
        # Reconstruct original record format
        memories = []
        for res in results:
            mem = {"context": res["text"]}
            mem.update(res["metadata"])
            mem["memory_id"] = res["id"]
            memories.append(mem)
        return memories
    
    def delete_memory(self, memory_id: str) -> None:
        """Remove a memory by ID."""
        self.adapter.delete(memory_id)
    
    def count(self) -> int:
        """Return total number of memories."""
        return self.adapter.count()
