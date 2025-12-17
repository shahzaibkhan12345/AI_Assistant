# backend/app/main.py

from fastapi import FastAPI
from app.api.v1.posts import router as posts_router # Import the router
from app.core.config import settings
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="AI Social Media Assistant API",
    description="An API to help manage and generate social media content.",
    version="1.0.0",
)
# --- ADD THIS MIDDLEWARE ---
# Configure CORS
origins = [
    "http://localhost:5173",  # The address of our React frontend
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# --- END OF MIDDLEWARE ---

#app.include_router(posts_router, prefix="/api/v1/posts", tags=["posts"])

app.include_router(posts_router, prefix="/api/v1/posts", tags=["posts"])

@app.get("/")
def read_root():
    return {"message": "Welcome to the AI Social Media Assistant API!"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}
