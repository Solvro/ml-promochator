from sqlmodel import SQLModel, Field
from pydantic import BaseModel


class Feedback(SQLModel, table=True):
    """
    Represents a feedback entry for a recommended supervisor.

    This model is stored in a database and contains information about:
    - The user's question regarding their thesis topic.
    - The recommended supervisor's name and faculty.
    - A flag indicating whether the recommendation was adequate.

    Attributes:
        id (int | None): Unique identifier of the feedback entry (auto-incremented).
        question (str): The original question related to the thesis topic.
        supervisor_name (str): Name of the recommended supervisor.
        faculty (str | None): Faculty to which the supervisor belongs (optional).
        is_adequate (bool): Indicates whether the recommendation was adequate.
    """
    id: int | None = Field(default=None, primary_key=True)
    question: str
    supervisor_name: str
    faculty: str | None = None
    is_adequate: bool


class FeedbackCreate(BaseModel):
    """
    Represents the input data for creating a new feedback entry.

    This model is used to validate and structure the data before inserting it into the database.

    Attributes:
        question (str): The original question related to the thesis topic.
        supervisor_name (str): Name of the recommended supervisor.
        faculty (str | None): Faculty to which the supervisor belongs (optional).
        is_adequate (bool): Indicates whether the recommendation was adequate.
    """
    question: str
    supervisor_name: str
    faculty: str | None = None
    is_adequate: bool
