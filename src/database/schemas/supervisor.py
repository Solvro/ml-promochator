from datetime import datetime

from pydantic import BaseModel
from sqlmodel import Field, SQLModel


class Supervisor(SQLModel, table=True):
    id: int = Field(primary_key=True)
    name: str
    faculty: str | None = None
    created_at: datetime = Field(
        default_factory=datetime.now,
    )


class SupervisorCreate(BaseModel):
    name: str
    faculty: str
