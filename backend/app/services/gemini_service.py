# backend/app/services/gemini_service.py

import time
from google import genai
from google.genai import errors as genai_errors
from app.core.config import settings

# Create a client with the API key
client = genai.Client(api_key=settings.GEMINI_API_KEY)

def generate_content(prompt: str) -> str:
    """
    Generates content using the Gemini model based on a given prompt.
    Uses the new google.genai package with retry logic.
    """
    # List of models to try in order of preference
    # Using models with different quota pools
    model_names = [
        'gemini-1.5-flash',         # Stable model - usually has better quota
        'gemini-1.5-flash-latest',  # Latest stable 1.5
        'gemini-1.5-pro',           # Pro model
        'gemini-2.0-flash-exp',     # Experimental 2.0 (might have quota issues)
    ]
    
    last_error = None
    
    for model_name in model_names:
        # Try each model with retries
        for attempt in range(3):
            try:
                print(f"Trying model: {model_name} (attempt {attempt + 1})")
                
                # Generate content using the new API
                response = client.models.generate_content(
                    model=model_name,
                    contents=prompt
                )
                
                # Return the generated text
                print(f"Success with model: {model_name}")
                return response.text

            except genai_errors.ClientError as e:
                error_str = str(e)
                print(f"Error with model {model_name}: {error_str}")
                
                # Check if it's a rate limit error
                if '429' in error_str or 'RESOURCE_EXHAUSTED' in error_str:
                    # Wait and retry with same model or try next model
                    if attempt < 2:
                        wait_time = (attempt + 1) * 5  # 5, 10 seconds
                        print(f"Rate limited, waiting {wait_time}s before retry...")
                        time.sleep(wait_time)
                        continue
                    else:
                        # Try next model
                        last_error = e
                        break
                else:
                    # Non-retryable error, try next model
                    last_error = e
                    break
                    
            except Exception as e:
                print(f"Unexpected error with model {model_name}: {e}")
                last_error = e
                break
    
    # If all models failed, return error message
    error_msg = str(last_error) if last_error else "Unknown error"
    print(f"All models failed. Last error: {error_msg}")
    
    if 'RESOURCE_EXHAUSTED' in error_msg or '429' in error_msg:
        return "API quota exceeded. Please wait a few minutes or check your Gemini API billing settings."
    
    return "Sorry, I had trouble generating content. Please check your API key and try again."