import re

def clean_text(text: str) -> str:
    """Normalize whitespace and strip common artifacts."""
    if not text:
        return ""
    # Replace multiple spaces/newlines with single ones
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def truncate_to_tokens(text: str, max_words: int = 500) -> str:
    """Crude truncation by word count as a proxy for tokens."""
    words = text.split()
    if len(words) <= max_words:
        return text
    return " ".join(words[:max_words]) + "..."

def combine_image_and_query(description: str, query: str) -> str:
    """Merge multimodal inputs for retrieval."""
    if not description:
        return query
    if not query:
        return f"Image description: {description}"
    return f"Image description: {description}\nUser query: {query}"
