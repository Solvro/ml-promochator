from langchain_core.messages import BaseMessage, RemoveMessage
from langchain_core.prompts import ChatPromptTemplate, HumanMessagePromptTemplate, SystemMessagePromptTemplate
from langgraph.graph.state import CompiledStateGraph

from src.components.models import InputRecommendationGeneration, Recommendation
from src.components.prompts import (
    GENERAL_PROMPT_TEMPLATE,
    OUTPUT_FORMAT_PROMPT,
    RETRIEVAL_INSTRUCTION_PROMPT,
    SYSTEM_PROMPT,
)


async def format_docs(docs):
    return '\n\n\n'.join([d.page_content for d in docs])


def print_messages(messages):
    for message in messages:
        print(message.pretty_print())


def format_prompt(query, history=None, retrieved_context='', faculty=''):
    """
    Returns FORMATTED messages (not a template) using the inputs.
    """
    if history is None:
        history = [BaseMessage(content='')]

    # Common templates
    human_template = HumanMessagePromptTemplate.from_template(
        GENERAL_PROMPT_TEMPLATE,
        input_variables=['retrieved_context', 'query', 'faculty'],
    )

    # Base message structure
    messages = []

    if retrieved_context.strip():  # if retrieved smth - command to format accordingly
        messages.append(SystemMessagePromptTemplate.from_template(SYSTEM_PROMPT + '\n' + OUTPUT_FORMAT_PROMPT))
    else:  # if it is the start of the graph(did not retrieved anything) - provide instructions on retrieval
        messages.append(SystemMessagePromptTemplate.from_template(SYSTEM_PROMPT + '\n' + RETRIEVAL_INSTRUCTION_PROMPT))

    # Add history and human template
    messages.extend(history)
    messages.append(human_template)

    prompt_template = ChatPromptTemplate.from_messages(messages)
    return prompt_template.format_messages(
        retrieved_context=retrieved_context,
        query=query.content,
        faculty=faculty,
    )


async def clear_memory(graph: CompiledStateGraph, thread_id: str) -> None:
    config = {'configurable': {'thread_id': thread_id}}

    try:
        messages = graph.get_state(config).values['messages']

        for message in messages:
            await graph.aupdate_state(config, {'messages': RemoveMessage(id=message.id)})
    except Exception:
        pass  # exception is thrown if memory is empty - "messages" key doesn't exist


async def run_graph(graph: CompiledStateGraph, input_model: InputRecommendationGeneration, thread_id: str):
    config = {'configurable': {'thread_id': thread_id}}

    final_state = await graph.ainvoke(
        {'faculty': input_model.faculty, 'messages': input_model.question},
        config=config,
    )

    if final_state.get('recommendation', {}):
        return final_state['recommendation']
    else:
        return Recommendation(hello_message=final_state['messages'][-1].content)
