from langchain_core.prompts import ChatPromptTemplate
from langchain_core.documents import Document
from langgraph.graph import END, StateGraph, START
from typing_extensions import TypedDict
from src.components.llms import chat_llm
from src.components.database import get_vectorstore
from src.components.constants import VECTORSTORE_PATH
from src.components.embeddings import openai_embeddings
from src.components.prompts import PROMPT_TEMPLATE, SYSTEM_PROMPT
from src.components.models import Recommendation

# Load vector database
vectorstore = get_vectorstore(VECTORSTORE_PATH, openai_embeddings)

# Define the prompt template for the AI model
template = ChatPromptTemplate(
    [
        ("system", SYSTEM_PROMPT),
        ("human", PROMPT_TEMPLATE),
    ]
)


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
    question: str
    retrieved_docs: list[Document]
    prompt: ChatPromptTemplate
    recommendation: Recommendation


async def _format_docs(docs):
    """
    Formats retrieved supervisor documents into a structured text format.

    Parameters:
        docs (list[Document]): List of documents retrieved from the vectorstore.

    Returns:
        str (str): Concatenated text of documents separated by three new lines
    """
    return "\n\n\n".join([d.page_content for d in docs])


async def route_retriever(state: RecommendationState):
    """
    Determines which retrieval function to use based on faculty presence.

    Parameters:
        state (RecommendationState): The current workflow state.

    Returns:
        str (str): The next step in the workflow ("retrieve_supervisors" or "retrieve_supervisors_by_faculty").
    """
    faculty = state["faculty"]

    if faculty is None:
        return "retrieve_supervisors"
    return "retrieve_supervisors_by_faculty"


async def retrieve_supervisors(state: RecommendationState):
    """
    Retrieves supervisors relevant to the given research question from the vector database.

    Parameters:
        state (RecommendationState): The current workflow state.

    Returns:
        RecommendationState: Updated state with retrieved supervisor documents.
    """
    question = state["question"]

    retrieved_docs = await vectorstore.amax_marginal_relevance_search(
        query=question,
        k=8,
    )

    return {**state, "retrieved_docs": retrieved_docs}


async def retrieve_supervisors_by_faculty(state: RecommendationState):
    """
    Retrieves supervisors from a specific faculty based on the research question.

    Parameters:
        state (RecommendationState): The current workflow state.

    Returns:
        RecommendationState: Updated state with retrieved supervisor documents.
    """
    faculty = state["faculty"]
    question = state["question"]

    retrieved_docs = await vectorstore.amax_marginal_relevance_search(
        query=question,
        k=8,
        filter={"faculty": faculty},
    )

    return {**state, "retrieved_docs": retrieved_docs}


async def fill_template(state: RecommendationState):
    """
    Formats the retrieved supervisor data into a structured AI prompt.

    Parameters:
        state (RecommendationState): The current workflow state.

    Returns:
        RecommendationState: Updated state with a formatted AI prompt.
    """
    question = state["question"]
    retrieved_docs = state["retrieved_docs"]
    retrieved_context = await _format_docs(retrieved_docs)

    prompt = template.format(question=question, retrieved_context=retrieved_context)

    return {**state, "prompt": prompt}


async def recommend(state: RecommendationState):
    """
    Generates a thesis supervisor recommendation using the AI model.

    Parameters:
        state (RecommendationState): The current workflow state.

    Returns:
        RecommendationState: Updated state with the AI-generated recommendation.
    """
    prompt = state["prompt"]
    recommendation = await chat_llm.ainvoke(prompt)

    return {**state, "recommendation": recommendation}

# Define the workflow graph
workflow = StateGraph(RecommendationState)

# Add retrieval nodes
workflow.add_node("retrieve_supervisors", retrieve_supervisors)
workflow.add_node("retrieve_supervisors_by_faculty", retrieve_supervisors_by_faculty)

# Add processing nodes
workflow.add_node("fill_template", fill_template)
workflow.add_node("recommend", recommend)

# Define workflow transitions
workflow.add_conditional_edges(
    START,
    route_retriever,
    {
        "retrieve_supervisors": "retrieve_supervisors",
        "retrieve_supervisors_by_faculty": "retrieve_supervisors_by_faculty",
    },
)
workflow.add_edge("retrieve_supervisors", "fill_template")
workflow.add_edge("retrieve_supervisors_by_faculty", "fill_template")
workflow.add_edge("fill_template", "recommend")
workflow.add_edge("recommend", END)

# Compile the workflow
recommendation_graph = workflow.compile()


if __name__ == "__main__":
    import asyncio

    final_state = asyncio.run(
        recommendation_graph.ainvoke(
            {
                "faculty": "Faculty of Information and Communication Technology",
                "question": "Recommend me supervisors for my thesis 'Deep Generative AI models'",
            }
        )
    )
    print(final_state["recommendation"].as_str)
