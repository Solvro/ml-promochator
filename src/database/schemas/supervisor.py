from datetime import datetime

from pydantic import BaseModel
from sqlmodel import Field, SQLModel


class Supervisor(SQLModel, table=True):
    """
    Represents a supervisor entity stored in the database.

    Attributes:
        id (int): Primary key, unique identifier of the supervisor.
        name (str): Full name of the supervisor.
        faculty (Optional[str]): Faculty the supervisor is associated with.
        created_at (datetime): Timestamp of creation.
    """

    id: int = Field(primary_key=True)
    name: str
    faculty: str | None = None
    created_at: datetime = Field(
        default_factory=datetime.now,
    )


class SupervisorCreate(BaseModel):
    """
    Input model for creating a new supervisor.

    Attributes:
        name (str): Full name of the supervisor.
        faculty (Optional[str]): Faculty the supervisor is associated with.
    """
    name: str
    faculty: str
