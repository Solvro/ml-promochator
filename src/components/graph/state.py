from typing import TypedDict, Annotated

from langchain_core.documents import Document
from langchain_core.messages import BaseMessage
from langgraph.graph import add_messages

from src.components.models import Recommendation


class RecommendationState(TypedDict):
    faculty: str | None
    messages: Annotated[list, add_messages]  # instead of simple question string

    should_retrieve: bool
    retrieving_query: str
    retrieved_docs: list[Document]
    recommendation: Recommendation

    prompt: list[BaseMessage]