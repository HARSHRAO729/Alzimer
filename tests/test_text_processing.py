from utils.text_processing import clean_text, truncate_to_tokens, combine_image_and_query

def test_clean_text():
    assert clean_text("  hello   world  \n") == "hello world"
    assert clean_text(None) == ""

def test_truncate_to_tokens():
    text = "one two three four five"
    assert truncate_to_tokens(text, max_words=3) == "one two three..."
    assert truncate_to_tokens(text, max_words=10) == text

def test_combine_image_and_query():
    desc = "A birthday cake"
    query = "When was this?"
    combined = combine_image_and_query(desc, query)
    assert "Image description: A birthday cake" in combined
    assert "User query: When was this?" in combined
    
    assert combine_image_and_query(None, query) == query
    assert combine_image_and_query(desc, None) == f"Image description: {desc}"
