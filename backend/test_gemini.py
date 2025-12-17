"""Quick test script for Gemini API"""
import os
import sys

# Set up the environment
os.chdir(os.path.dirname(os.path.abspath(__file__)))

from app.core.config import settings

print(f"API Key loaded: {settings.GEMINI_API_KEY[:15]}...")

try:
    from google import genai
    print("Using new google.genai package")
    
    client = genai.Client(api_key=settings.GEMINI_API_KEY)
    
    # List available models first
    print("\nAvailable models:")
    for model in list(client.models.list())[:5]:
        print(f"  - {model.name}")
    
    print("\nTrying to generate content...")
    response = client.models.generate_content(
        model='gemini-2.0-flash-exp',
        contents='Say hello in exactly 3 words'
    )
    print(f"Success! Response: {response.text}")
    
except Exception as e:
    print(f"Error: {type(e).__name__}: {e}")
    import traceback
    traceback.print_exc()
