from src.components.graph.state import RecommendationState

from langchain_core.messages import AIMessage
from langgraph.graph import END

from src.components.llms import chat_llm, chat_llm_with_structured
from src.components.prompts import route_to_retriever_placeholder
from src.components.graph.utils import format_prompt, format_docs

from src.components.constants import VECTORSTORE_PATH
from src.components.database import get_vectorstore
from src.components.embeddings import openai_embeddings

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

        return {**state, 'retrieving_query': response, 'should_retrieve': True,
                'recommendation': None}
    else:
        return {**state, 'messages': [response], 'should_retrieve': False,
                'recommendation': None}


# Decides whether to retrieve docs, or proceed to END
async def route_retriever(state: RecommendationState):
    should_retrieve = state['should_retrieve']
    if should_retrieve:
        return 'retrieve_supervisors'
    else:
        return END


async def retrieve_supervisors(state: RecommendationState):
    faculty = state.get('faculty', None)
    question = state['messages'][-1].content

    retrieved_docs = await vectorstore.amax_marginal_relevance_search(
        query=question,
        k=8,
        filter={'faculty': faculty} if state['faculty'] is not None else {},
    )

    return {**state, 'retrieved_docs': retrieved_docs}


async def fill_template(state: RecommendationState):
    query = state['messages'][-1]

    retrieved_context = ''

    if state['should_retrieve']:
        retrieved_docs = state['retrieved_docs']
        retrieved_context = await format_docs(retrieved_docs)

    prompt = format_prompt(query=query, retrieved_context=retrieved_context, history=state['messages'][:-1],
                           faculty=state.get('faculty', ''))

    return {**state, 'prompt': prompt}


async def final_answer(state: RecommendationState):
    prompt = state['prompt']
    response = await chat_llm_with_structured.ainvoke(prompt)

    return {**state, 'messages': [AIMessage(response.as_str)], 'recommendation': response}
