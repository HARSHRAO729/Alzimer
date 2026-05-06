import pytest
from core.retriever import MemoryRetriever

def test_build_context(seeded_db):
    retriever = MemoryRetriever(seeded_db)
    results = retriever.retrieve("testing")
    context = retriever.build_context(results)
    
    assert "--- Memory 1 ---" in context
    assert "Testing the memory store" in context
    assert "Emotional Tone: Neutral" in context

def test_build_context_empty():
    from adapters.chroma_adapter import ChromaVectorStore
    import config
    # Use a dummy adapter with no data
    adapter = ChromaVectorStore(collection_name="empty", persist_dir="data/test_empty")
    retriever = MemoryRetriever(adapter)
    context = retriever.build_context([])
    assert "No relevant memories found" in context
