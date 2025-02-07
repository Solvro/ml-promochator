from typing import Annotated
from dotenv import load_dotenv
from langgraph.checkpoint.base import Checkpoint, empty_checkpoint, ChannelVersions

from src.components.models import InputRecommendationGeneration, Recommendation

load_dotenv()

from langchain_core.documents import Document
from langchain_core.messages import BaseMessage, RemoveMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import END, START, StateGraph, add_messages
from typing_extensions import TypedDict

from src.components.constants import VECTORSTORE_PATH
from src.components.database import get_vectorstore
from src.components.embeddings import openai_embeddings
from src.components.llms import chat_llm, chat_llm_with_structured
from src.components.prompts import GENERAL_PROMPT_TEMPLATE, SYSTEM_PROMPT, RETRIEVAL_INSTRUCTION_PROMPT, \
    OUTPUT_FORMAT_PROMPT, route_to_retriever_placeholder

vectorstore = get_vectorstore(VECTORSTORE_PATH, openai_embeddings)


def format_prompt(query, history=None, retrieved_context='', faculty=''):
    """
    Returns FORMATTED messages (not a template) using the inputs.
    """
    if history is None:
        history = [BaseMessage(content='')]

    # Common templates
    human_template = HumanMessagePromptTemplate.from_template(
        GENERAL_PROMPT_TEMPLATE,
        input_variables=["retrieved_context", "query", "faculty"],
    )

    # Base message structure
    messages = []

    if retrieved_context.strip():  # if retrieved smth - command to format accordingly
        messages.append(SystemMessagePromptTemplate.from_template(SYSTEM_PROMPT + "\n" + OUTPUT_FORMAT_PROMPT))
    else:  # if it is the start of the graph(did not retrieved anything) - provide instructions on retrieval
        messages.append(SystemMessagePromptTemplate.from_template(SYSTEM_PROMPT + "\n" + RETRIEVAL_INSTRUCTION_PROMPT))

    # Add history and human template
    messages.extend(history)
    messages.append(human_template)

    prompt_template = ChatPromptTemplate.from_messages(messages)
    return prompt_template.format_messages(
        retrieved_context=retrieved_context,
        query=query.content,
        faculty=faculty,
    )


class RecommendationState(TypedDict):
    faculty: str | None
    messages: Annotated[list, add_messages]  # instead of simple question string

    should_retrieve: bool
    retrieving_query: str
    retrieved_docs: list[Document]
    recommendation: Recommendation

    prompt: list[BaseMessage]


async def _format_docs(docs):
    return '\n\n\n'.join([d.page_content for d in docs])


def print_messages(messages):
    for message in messages:
        print(message.pretty_print())


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
        faculty = state['faculty']

        if faculty is None:
            return 'retrieve_supervisors'
        return 'retrieve_supervisors_by_faculty'
    else:
        return END


async def retrieve_supervisors(state: RecommendationState):
    question = state['messages'][-1].content

    retrieved_docs = await vectorstore.amax_marginal_relevance_search(
        query=question,
        k=8,
    )

    return {**state, 'retrieved_docs': retrieved_docs}


async def retrieve_supervisors_by_faculty(state: RecommendationState):
    faculty = state['faculty']
    question = state['messages'][-1].content

    retrieved_docs = await vectorstore.amax_marginal_relevance_search(
        query=question,
        k=8,
        filter={'faculty': faculty},
    )

    return {**state, 'retrieved_docs': retrieved_docs}


async def fill_template(state: RecommendationState):
    query = state['messages'][-1]

    retrieved_context = ''

    if state['should_retrieve']:
        retrieved_docs = state['retrieved_docs']
        retrieved_context = await _format_docs(retrieved_docs)

    prompt = format_prompt(query=query, retrieved_context=retrieved_context, history=state['messages'][:-1],
                           faculty=state.get('faculty', ''))

    return {**state, 'prompt': prompt}


async def final_answer(state: RecommendationState):
    prompt = state['prompt']
    response = await chat_llm_with_structured.ainvoke(prompt)

    return {**state, 'messages': [AIMessage(response.as_str)], 'recommendation': response}


workflow = StateGraph(RecommendationState)

workflow.add_node('chatbot', chatbot)
workflow.add_node('retrieve_supervisors', retrieve_supervisors)
workflow.add_node('retrieve_supervisors_by_faculty', retrieve_supervisors_by_faculty)
workflow.add_node('fill_template', fill_template)
workflow.add_node('final_answer', final_answer)

workflow.add_edge(START, 'chatbot')
workflow.add_conditional_edges(
    'chatbot',
    route_retriever,
    {
        'retrieve_supervisors': 'retrieve_supervisors',
        'retrieve_supervisors_by_faculty': 'retrieve_supervisors_by_faculty',
        END: END
    },
)
workflow.add_edge('retrieve_supervisors', 'fill_template')
workflow.add_edge('retrieve_supervisors_by_faculty', 'fill_template')
workflow.add_edge('fill_template', 'final_answer')
workflow.add_edge('final_answer', END)

memory_saver = MemorySaver()


async def clear_memory(thread_id: str) -> None:
    config = {'configurable': {'thread_id': thread_id}}

    try:
        messages = recommendation_graph.get_state(config).values["messages"]

        for message in messages:
            await recommendation_graph.aupdate_state(config, {"messages": RemoveMessage(id=message.id)})
    except Exception as e:
        pass # exception is thrown if memory is empty - "messages" key doesn't exist




recommendation_graph = workflow.compile(
    checkpointer=memory_saver
)  # adding checkpointer, affects the way how "messages" field is built


async def run_graph(input_model: InputRecommendationGeneration, thread_id: str):
    config = {'configurable': {'thread_id': thread_id}}

    final_state = await recommendation_graph.ainvoke(
        {
            "faculty": input_model.faculty,
            "messages": input_model.question
        },
        config=config,
    )

    if final_state.get('recommendation', {}):
        return final_state['recommendation']
    else:
        return Recommendation(hello_message=final_state['messages'][-1].content)


if __name__ == '__main__':
    import asyncio

    thread_id = '1'

    while True:
        query = input('You: ')
        request_data = InputRecommendationGeneration(question=query,
                                                     faculty="Faculty of Information and Communication Technology")

        result = asyncio.run(run_graph(request_data, thread_id))

        print('Chat: ' + result.as_str)
