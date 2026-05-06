import json
from pathlib import Path
from typing import Any, Dict, List

def load_json(path: str | Path) -> Any:
    """Load and parse a JSON file."""
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_json(path: str | Path, data: Any) -> None:
    """Save data to a JSON file."""
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def ensure_dir(path: str | Path) -> None:
    """Ensure a directory exists."""
    Path(path).mkdir(parents=True, exist_ok=True)
