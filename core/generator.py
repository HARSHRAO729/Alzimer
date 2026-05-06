import ollama
import config
from core.prompts import SYSTEM_PROMPT, GENERATE_PROMPT_TEMPLATE
from typing import Generator, Optional, List, Dict

def generate_response(query: str, context: str, chat_history: Optional[List[Dict[str, str]]] = None) -> Generator[str, None, None]:
    """Generate a streaming response from Gemma 4 via Ollama."""
    
    full_prompt = GENERATE_PROMPT_TEMPLATE.format(
        system_prompt=SYSTEM_PROMPT,
        context=context,
        query=query
    )
    
    messages = []
    if chat_history:
        messages.extend(chat_history)
    
    messages.append({'role': 'user', 'content': full_prompt})
    
    try:
        response_stream = ollama.chat(
            model=config.LLM_MODEL,
            messages=messages,
            stream=True,
            options={'temperature': config.GENERATION_TEMP}
        )
        
        for chunk in response_stream:
            yield chunk['message']['content']
            
    except Exception as e:
        yield f"I'm sorry, I encountered an error connecting to my memory core: {e}"
