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


vectorstore = get_vectorstore(VECTORSTORE_PATH, openai_embeddings)

template = ChatPromptTemplate(
    [
        ("system", SYSTEM_PROMPT),
        ("human", PROMPT_TEMPLATE),
    ]
)


class RecommendationState(TypedDict):
    faculty: str | None
    question: str
    retrieved_docs: list[Document]
    prompt: ChatPromptTemplate
    recommendation: Recommendation


async def _format_docs(docs):
    return "\n\n\n".join([d.page_content for d in docs])


async def route_retriever(state: RecommendationState):
    faculty = state["faculty"]

    if faculty is None:
        return "retrieve_supervisors"
    return "retrieve_supervisors_by_faculty"


async def retrieve_supervisors(state: RecommendationState):
    question = state["question"]

    retrieved_docs = await vectorstore.amax_marginal_relevance_search(
        query=question,
        k=8,
    )

    return {**state, "retrieved_docs": retrieved_docs}


async def retrieve_supervisors_by_faculty(state: RecommendationState):
    faculty = state["faculty"]
    question = state["question"]

    retrieved_docs = await vectorstore.amax_marginal_relevance_search(
        query=question,
        k=8,
        filter={"faculty": faculty},
    )

    return {**state, "retrieved_docs": retrieved_docs}


async def fill_template(state: RecommendationState):
    question = state["question"]
    retrieved_docs = state["retrieved_docs"]
    retrieved_context = await _format_docs(retrieved_docs)

    prompt = template.format(question=question, retrieved_context=retrieved_context)

    return {**state, "prompt": prompt}


async def recommend(state: RecommendationState):
    prompt = state["prompt"]
    recommendation = await chat_llm.ainvoke(prompt)

    return {**state, "recommendation": recommendation}


workflow = StateGraph(RecommendationState)

workflow.add_node("retrieve_supervisors", retrieve_supervisors)
workflow.add_node("retrieve_supervisors_by_faculty", retrieve_supervisors_by_faculty)
workflow.add_node("fill_template", fill_template)
workflow.add_node("recommend", recommend)

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
