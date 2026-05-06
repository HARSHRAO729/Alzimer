from typing import List, Dict, Any
from adapters.base import VectorStoreAdapter
import config

class MemoryRetriever:
    """Retriever for assembly of memory context."""
    
    def __init__(self, adapter: VectorStoreAdapter):
        self.adapter = adapter
    
    def retrieve(self, query: str, top_k: int = config.TOP_K) -> List[Dict[str, Any]]:
        """Retrieve top-K similar memories from the store."""
        return self.adapter.query(query, top_k=top_k)
    
    def build_context(self, results: List[Dict[str, Any]]) -> str:
        """Format retrieved results into a structured context block."""
        if not results:
            return "No relevant memories found in the archive."
        
        context_parts = []
        for i, res in enumerate(results, 1):
            meta = res["metadata"]
            part = f"--- Memory {i} ---\n"
            part += f"Date: {meta.get('date', 'Unknown')}\n"
            part += f"Emotional Tone: {meta.get('emotional_tone', 'Unknown')}\n"
            part += f"People involved: {', '.join(meta.get('people', []))}\n"
            part += f"Context: {res['text']}\n"
            context_parts.append(part)
            
        return "\n".join(context_parts)
