# backend/app/services/ai_service.py
# Using Groq API for fast LLM inference

from groq import Groq
from app.core.config import settings

# Create a Groq client with the API key
client = Groq(api_key=settings.GROQ_API_KEY)

def generate_content(prompt: str) -> str:
    """
    Generates content using the Groq API with fast inference.
    """
    try:
        print(f"Generating content with Groq API...")
        
        # Create the chat completion - using llama-3.1-8b for FAST inference
        completion = client.chat.completions.create(
            model="llama-3.1-8b-instant",  # Very fast model!
            messages=[
                {
                    "role": "system",
                    "content": "You are a social media content expert. Generate engaging, platform-appropriate content based on the user's request. Keep your response concise and ready to post. Do not include any thinking or reasoning - just output the post content directly."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.7,
            max_tokens=512,  # Shorter for faster response
        )
        
        # Get the generated text
        generated_text = completion.choices[0].message.content
        print(f"Success! Generated {len(generated_text)} characters")
        
        return generated_text

    except Exception as e:
        error_msg = str(e)
        print(f"Error calling Groq API: {error_msg}")
        
        if 'rate_limit' in error_msg.lower() or '429' in error_msg:
            return "API rate limit exceeded. Please wait a moment and try again."
        
        return f"Sorry, I had trouble generating content. Error: {error_msg}"
