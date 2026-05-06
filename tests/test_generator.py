import pytest
from unittest.mock import patch, MagicMock
from core.generator import generate_response

@patch('ollama.chat')
def test_generate_response_streaming(mock_chat):
    # Mock the streaming response
    mock_chat.return_value = [
        {'message': {'content': 'Hello'}},
        {'message': {'content': ' world'}}
    ]
    
    query = "hi"
    context = "some context"
    
    responses = list(generate_response(query, context))
    
    assert responses == ["Hello", " world"]
    mock_chat.assert_called_once()
    
    # Verify the prompt passed to ollama
    call_args = mock_chat.call_args
    messages = call_args[1]['messages']
    last_message = messages[-1]['content']
    assert "USER QUERY:\nhi" in last_message
    assert "CONTEXT MEMORIES:\nsome context" in last_message

@patch('ollama.chat')
def test_generate_response_error(mock_chat):
    mock_chat.side_effect = Exception("Ollama down")
    
    responses = list(generate_response("hi", "context"))
    assert "error connecting to my memory core" in responses[0]
