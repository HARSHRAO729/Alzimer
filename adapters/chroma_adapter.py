import chromadb
from chromadb.utils import embedding_functions
from typing import List, Dict, Any
from adapters.base import VectorStoreAdapter
import config

class ChromaVectorStore(VectorStoreAdapter):
    """ChromaDB implementation of the vector store interface."""
    
    def __init__(self, collection_name: str = config.COLLECTION_NAME, persist_dir: str = str(config.CHROMA_DIR)):
        self.client = chromadb.PersistentClient(path=persist_dir)
        self.embedding_fn = embedding_functions.SentenceTransformerEmbeddingFunction(
            model_name=config.EMBEDDING_MODEL
        )
        self.collection = self.client.get_or_create_collection(
            name=collection_name,
            embedding_function=self.embedding_fn
        )
    
    def upsert(self, id: str, text: str, metadata: Dict[str, Any]) -> None:
        self.collection.upsert(
            ids=[id],
            documents=[text],
            metadatas=[metadata]
        )
    
    def query(self, query_text: str, top_k: int = config.TOP_K) -> List[Dict[str, Any]]:
        results = self.collection.query(
            query_texts=[query_text],
            n_results=top_k
        )
        
        formatted_results = []
        if results['ids'] and results['ids'][0]:
            for i in range(len(results['ids'][0])):
                formatted_results.append({
                    "id": results['ids'][0][i],
                    "text": results['documents'][0][i],
                    "metadata": results['metadatas'][0][i],
                    "distance": results['distances'][0][i] if 'distances' in results else None
                })
        return formatted_results
    
    def delete(self, id: str) -> None:
        self.collection.delete(ids=[id])
    
    def list_all(self) -> List[Dict[str, Any]]:
        results = self.collection.get()
        formatted_results = []
        for i in range(len(results['ids'])):
            formatted_results.append({
                "id": results['ids'][i],
                "text": results['documents'][i],
                "metadata": results['metadatas'][i]
            })
        return formatted_results
    
    def count(self) -> int:
        return self.collection.count()
