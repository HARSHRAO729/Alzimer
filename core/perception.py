import ollama
import config
from typing import Optional

def describe_image(image_path: str) -> Optional[str]:
    """Generate a rich text description of an image using local LLaVA."""
    try:
        response = ollama.chat(
            model=config.VISION_MODEL,
            messages=[{
                'role': 'user',
                'content': 'Describe this image as if you are recalling a cherished memory. Include details about people, emotions, setting, colors, and atmosphere.',
                'images': [image_path]
            }]
        )
        return response['message']['content']
    except Exception as e:
        print(f"Error in perception engine: {e}")
        return None
