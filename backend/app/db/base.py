# backend/app/db/base.py

from sqlalchemy.orm import declarative_base

# This creates a base class that our models will inherit from.
Base = declarative_base()