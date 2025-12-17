# backend/app/models/post.py

from sqlalchemy import Column, Integer, String, DateTime, Text
from sqlalchemy.sql import func
from app.db.base import Base

class Post(Base):
    """
    Represents a social media post in the database.
    """
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    prompt = Column(String, nullable=False)
    platform = Column(String, nullable=False)
    tone = Column(String, nullable=False)
    generated_content = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
