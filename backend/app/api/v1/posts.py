# backend/app/api/v1/posts.py

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.schemas.post import PostCreateRequest, PostGenerationResponse, PostResponse
from app.services.ai_service import generate_content
from app.models.post import Post as PostModel
from app.services.twitter_service import post_tweet # <-- ADD THIS IMPORT

# --- CORRECTED IMPORT ---
# Import get_db from the correct file where we defined it
from app.db.session import get_db

# Create a router for the posts endpoints
router = APIRouter()

@router.post("/generate", response_model=PostGenerationResponse)
def create_post(request: PostCreateRequest, db: Session = Depends(get_db)): # --- ADDED db PARAMETER ---
    """
    Takes a prompt, generates a post, and saves it to the database.
    """
    # You can make the prompt more sophisticated based on platform/tone
    # For now, we'll keep it simple.
    detailed_prompt = f"Generate a {request.tone} social media post for {request.platform} based on this idea: {request.prompt}"

    generated_content = generate_content(detailed_prompt)

    if "Sorry, I had trouble" in generated_content:
        # If the service returned an error, raise an HTTP exception
        raise HTTPException(status_code=500, detail=generated_content)

    # --- NEW: Save to database ---
    db_post = PostModel(
        prompt=request.prompt,
        platform=request.platform,
        tone=request.tone,
        generated_content=generated_content
    )
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    # --- End of new code ---

    # Return the generated content in the specified response format
    return PostGenerationResponse(
        generated_content=generated_content,
        platform=request.platform,
        tone=request.tone
    )


@router.get("/", response_model=list[PostResponse])
def get_all_posts(db: Session = Depends(get_db)):
    """
    Retrieve all posts saved in the database.
    """
    posts = db.query(PostModel).all()
    return posts
@router.post("/{post_id}/publish")
def publish_post(post_id: int, db: Session = Depends(get_db)):
    """
    Publishes a specific saved post to Twitter.
    """
    # 1. Find the post in the database
    db_post = db.query(PostModel).filter(PostModel.id == post_id).first()
    if not db_post:
        raise HTTPException(status_code=404, detail="Post not found")

    # 2. Call the Twitter service to post the content
    success = post_tweet(db_post.generated_content)

    if success:
        return {"message": f"Post '{db_post.prompt}' successfully published to Twitter!"}
    else:
        raise HTTPException(status_code=500, detail="Failed to publish post to Twitter.")