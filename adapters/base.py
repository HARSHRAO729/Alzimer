from abc import ABC, abstractmethod
from typing import List, Dict, Any

class VectorStoreAdapter(ABC):
    """Abstract interface for all vector store backends.
    
    Core logic calls these methods — never a concrete DB client.
    Swap ChromaDB for Pinecone/FAISS/PostgreSQL by writing 
    a new adapter that implements this interface.
    """
    
    @abstractmethod
    def upsert(self, id: str, text: str, metadata: Dict[str, Any]) -> None:
        """Store a document with its embedding."""
        pass
    
    @abstractmethod
    def query(self, query_text: str, top_k: int = 3) -> List[Dict[str, Any]]:
        """Retrieve top-K similar documents."""
        pass
    
    @abstractmethod
    def delete(self, id: str) -> None:
        """Remove a document by ID."""
        pass
    
    @abstractmethod
    def list_all(self) -> List[Dict[str, Any]]:
        """Return all stored documents."""
        pass
    
    @abstractmethod
    def count(self) -> int:
        """Return total document count."""
        pass
