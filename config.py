import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# Project Paths
BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"
CHROMA_DIR = DATA_DIR / "chroma_db"
MEMORIES_JSON = DATA_DIR / "memories.json"

# Ollama Config
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
LLM_MODEL = os.getenv("LLM_MODEL", "gemma4")
VISION_MODEL = os.getenv("VISION_MODEL", "llava")

# Embedding Config
EMBEDDING_MODEL = "all-MiniLM-L6-v2"
COLLECTION_NAME = "memories"

# RAG Config
TOP_K = 3
GENERATION_TEMP = 0.7

# Ensure directories exist
DATA_DIR.mkdir(exist_ok=True)
CHROMA_DIR.mkdir(exist_ok=True)
