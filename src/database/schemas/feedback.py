from sqlmodel import SQLModel, Field


class Feedback(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    question: str
    supervisor_name: str
    faculty: str | None = None
    is_adequate: bool
