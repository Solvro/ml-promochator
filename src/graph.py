from typing import Annotated
from dotenv import load_dotenv

load_dotenv()

from langchain_core.documents import Document
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage, BaseMessage
from langchain_core.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, PromptTemplate, \
    HumanMessagePromptTemplate
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import END, START, StateGraph, add_messages
from typing_extensions import TypedDict

from src.components.constants import VECTORSTORE_PATH
from src.components.database import get_vectorstore
from src.components.embeddings import openai_embeddings
from src.components.llms import chat_llm
from src.components.prompts import GENERAL_PROMPT_TEMPLATE, SYSTEM_PROMPT, RETRIEVAL_INSTRUCTION_PROMPT, \
    OUTPUT_FORMAT_PROMPT, route_to_retriever_placeholder

vectorstore = get_vectorstore(VECTORSTORE_PATH, openai_embeddings)


def format_prompt(query, history=None, retrieved_context=''):
    """
    Returns FORMATTED messages (not a template) using the inputs.
    """
    if history is None:
        history = [BaseMessage(content='')]

    # Common templates
    human_template = HumanMessagePromptTemplate.from_template(
        GENERAL_PROMPT_TEMPLATE,
        input_variables=["retrieved_context", "query"]
    )

    # Base message structure
    messages = []

    if retrieved_context.strip(): # if retrieved smth - command to format accordingly
            messages.append(SystemMessagePromptTemplate.from_template(SYSTEM_PROMPT + "\n" + OUTPUT_FORMAT_PROMPT))
    else: # if it is the start of the graph(did not retrieved anything) - provide instructions on retrieval
        messages.append(SystemMessagePromptTemplate.from_template(SYSTEM_PROMPT + "\n" + RETRIEVAL_INSTRUCTION_PROMPT))

    # Add history and human template
    messages.extend(history)
    messages.append(human_template)

    prompt_template = ChatPromptTemplate.from_messages(messages)
    return prompt_template.format_messages(
        retrieved_context=retrieved_context,
        query=query.content
    )


class RecommendationState(TypedDict):
    faculty: str | None
    messages: Annotated[list, add_messages]  # instead of simple question string

    should_retrieve: bool
    retrieving_query: str
    retrieved_docs: list[Document]

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

    print_messages(state['messages'])

    if route_to_retriever_placeholder in response.content:
        response.content = response.content.replace(
            route_to_retriever_placeholder, ''
        )  # removing placeholder from response

        return {**state, 'retrieving_query': response, 'should_retrieve': True}
    else:
        return {**state, 'messages': [response]}


# Decides whether to retrieve docs, or proceed to filling template for final answer
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

    prompt = format_prompt(query=query, retrieved_context=retrieved_context, history=state['messages'][:-1])

    return {**state, 'prompt': prompt, 'should_retrieve': False}  # resetting should_retrieve back to initial state


async def final_answer(state: RecommendationState):
    prompt = state['prompt']
    response = await chat_llm.ainvoke(prompt)

    return {**state, 'messages': [response]}


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


def load_memory():
    return MemorySaver()


recommendation_graph = workflow.compile(
    checkpointer=load_memory()
)  # adding checkpointer, affects the way how "messages" field is built??

if __name__ == '__main__':
    import asyncio

    config = {'configurable': {'thread_id': 1}}

    while True:
        query = input('You: ')

        final_state = asyncio.run(
            recommendation_graph.ainvoke(
                {
                    "faculty": "Faculty of Information and Communication Technology",
                    'messages': query,
                    'should_retrieve': False,
                    # by default, we don't want to retrieve anything, unless model specifies need for this
                },
                config=config,
            )
        )
        print('Chat: ' + final_state['messages'][-1].content)
