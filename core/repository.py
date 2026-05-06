from typing import List, Dict, Any, Generator
from core.memory_store import MemoryStore
from core.retriever import MemoryRetriever
from core.generator import generate_response
from adapters.base import VectorStoreAdapter

class MemoryRepository:
    """Unified entry point for all memory and assistant operations.
    
    This layer abstracts away the specific Store and Retriever classes,
    providing a clean API for the UI layer.
    """
    
    def __init__(self, adapter: VectorStoreAdapter):
        self.store = MemoryStore(adapter)
        self.retriever = MemoryRetriever(adapter)
    
    def add_memory(self, record: Dict[str, Any]) -> None:
        """Log a new life snapshot."""
        self.store.add_memory(record)
        
    def get_history(self) -> List[Dict[str, Any]]:
        """Retrieve the full chronological event log."""
        return self.store.get_timeline()
        
    def count(self) -> int:
        """Return total memory count."""
        return self.store.count()
        
    def reseed(self) -> int:
        """Reload foundational memories."""
        return self.store.load_seed_data()
        
    def query_assistant(self, prompt: str, chat_history: List[Dict[str, str]] = None) -> Generator[str, None, None]:
        """The core intelligence loop: Retrieve -> Context -> Generate."""
        results = self.retriever.retrieve(prompt)
        context = self.retriever.build_context(results)
        return generate_response(prompt, context, chat_history or [])

    def get_related_memories(self, prompt: str) -> List[Dict[str, Any]]:
        """Just retrieve relevant memories without generating a response."""
        return self.retriever.retrieve(prompt)
