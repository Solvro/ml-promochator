import uuid
from typing import Any, Dict, List, Optional

from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import JSONB
from sqlmodel import  SQLModel ,Field, Relationship
from pgvector.sqlalchemy import Vector

from app.core.config import settings

class Supervisor(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    full_name: str = Field(min_length=1, max_length=255)
    faculty: str = Field(min_length=1, max_length=255)
    interests: str | None = Field(default=None, max_length=255)
    research_papers: Optional[Dict[str, Any]] = Field(sa_column=Field(JSONB))
    supervisor_papers: Optional[Dict[str, Any]] = Field(sa_column=Field(JSONB))
    
    chunks: List["TextChunk"] = Relationship(back_populates="supervisor")


class TextChunk(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    page_content: str
    embedding: Optional[Vector] = Field(sa_column=Vector(settings.EMBEDDINGS_DIM))    
    supervisor_id: int = Field(default=None, foreign_key="supervisor.id")
    supervisor: Supervisor = Relationship(back_populates="chunks")
