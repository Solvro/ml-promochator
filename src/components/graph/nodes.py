from langchain_core.messages import AIMessage
from langgraph.graph import END

from src.components.constants import VECTORSTORE_PATH
from src.components.database import get_vectorstore
from src.components.embeddings import openai_embeddings
from src.components.graph.state import RecommendationState
from src.components.graph.utils import format_docs, format_prompt
from src.components.llms import chat_llm, chat_llm_with_structured
from src.components.prompts import route_to_retriever_placeholder

vectorstore = get_vectorstore(VECTORSTORE_PATH, openai_embeddings)


async def chatbot(state: RecommendationState):
    prompt = format_prompt(
        query=state['messages'][-1], history=state['messages'][:-1]
    )  # Appending whole chat history to the prompt
    response = await chat_llm.ainvoke(prompt)

    # print_messages(state['messages'])

    if route_to_retriever_placeholder in response.content:
        response.content = response.content.replace(
            route_to_retriever_placeholder, ''
        )  # removing placeholder from response

        return {**state, 'retrieving_query': response, 'should_retrieve': True, 'recommendation': None}
    else:
        return {**state, 'messages': [response], 'should_retrieve': False, 'recommendation': None}


# Decides whether to retrieve docs, or proceed to END
async def route_retriever(state: RecommendationState):
    """
    Determines which retrieval function to use based on faculty presence.

    Parameters:
        state (RecommendationState): The current workflow state.

    Returns:
        str (str): The next step in the workflow ("retrieve_supervisors" or "retrieve_supervisors_by_faculty").
    """
    should_retrieve = state['should_retrieve']
    if should_retrieve:
        return 'retrieve_supervisors'
    else:
        return END


async def retrieve_supervisors(state: RecommendationState):
    """
    Retrieves supervisors relevant to the given research question from the vector database.

    Parameters:
        state (RecommendationState): The current workflow state.

    Returns:
        RecommendationState: Updated state with retrieved supervisor documents.
    """
    faculty = state.get('faculty', None)
    question = state['messages'][-1].content

    retrieved_docs = await vectorstore.amax_marginal_relevance_search(
        query=question,
        k=8,
        filter={'faculty': faculty} if state['faculty'] is not None else {},
    )

    return {**state, 'retrieved_docs': retrieved_docs}


async def fill_template(state: RecommendationState):
    """
    Formats the retrieved supervisor data into a structured AI prompt.

    Parameters:
        state (RecommendationState): The current workflow state.

    Returns:
        RecommendationState: Updated state with a formatted AI prompt.
    """
    query = state['messages'][-1]

    retrieved_context = ''

    if state['should_retrieve']:
        retrieved_docs = state['retrieved_docs']
        retrieved_context = await format_docs(retrieved_docs)

    prompt = format_prompt(
        query=query,
        retrieved_context=retrieved_context,
        history=state['messages'][:-1],
        faculty=state.get('faculty', ''),
    )

    return {**state, 'prompt': prompt}


async def final_answer(state: RecommendationState):
    """
    Generates a thesis supervisor recommendation using the AI model.

    Parameters:
        state (RecommendationState): The current workflow state.

    Returns:
        RecommendationState: Updated state with the AI-generated recommendation.
    """
    prompt = state['prompt']
    response = await chat_llm_with_structured.ainvoke(prompt)

    return {**state, 'messages': [AIMessage(response.as_str)], 'recommendation': response}
