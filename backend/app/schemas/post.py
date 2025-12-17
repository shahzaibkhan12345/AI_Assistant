# backend/app/schemas/post.py

from datetime import datetime
from pydantic import BaseModel

# This schema defines the expected body of a POST request to generate a post
class PostCreateRequest(BaseModel):
    prompt: str
    platform: str = "twitter"  # Optional: can be twitter, linkedin, etc.
    tone: str = "professional" # Optional: can be funny, witty, professional

# This schema defines the shape of the successful response
class PostGenerationResponse(BaseModel):
    generated_content: str
    platform: str
    tone: str

# Schema for returning post data from the database
class PostResponse(BaseModel):
    id: int
    prompt: str
    platform: str
    tone: str
    generated_content: str
    created_at: datetime

    class Config:
        from_attributes = True  # This tells Pydantic to read from ORM objects