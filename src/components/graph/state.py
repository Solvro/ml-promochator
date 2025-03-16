from typing import Annotated, TypedDict

from langchain_core.documents import Document
from langchain_core.messages import BaseMessage
from langgraph.graph import add_messages

from src.components.models import Recommendation


class RecommendationState(TypedDict):
    """
    Represents the state of the recommendation workflow.

    Attributes:
        faculty (Optional[str]): The faculty to filter supervisors by (if provided).
        question (str): The research topic or query provided by the user.
        retrieved_docs (list[Document]): List of retrieved supervisor documents.
        prompt (ChatPromptTemplate): The formatted prompt for the AI model.
        recommendation (Recommendation): The final AI-generated supervisor recommendation.
    """
    faculty: str | None
    messages: Annotated[list, add_messages]  # instead of simple question string

    should_retrieve: bool
    retrieving_query: str
    retrieved_docs: list[Document]
    recommendation: Recommendation

    prompt: list[BaseMessage]
