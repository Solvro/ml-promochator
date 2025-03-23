from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import END, START, StateGraph

from src.components.graph.nodes import chatbot, fill_template, final_answer, retrieve_supervisors, route_retriever
from src.components.graph.state import RecommendationState
from src.components.graph.utils import run_graph
from src.components.models import InputRecommendationGeneration


def create_recommendation_workflow():
    """
    Creates and returns the recommendation workflow graph.

    Returns:
        StateGraph: The compiled recommendation workflow graph.
    """
    workflow = StateGraph(RecommendationState)

    workflow.add_node('chatbot', chatbot)
    workflow.add_node('retrieve_supervisors', retrieve_supervisors)
    workflow.add_node('fill_template', fill_template)
    workflow.add_node('final_answer', final_answer)

    workflow.add_edge(START, 'chatbot')
    workflow.add_conditional_edges(
        'chatbot',
        route_retriever,
        {'retrieve_supervisors': 'retrieve_supervisors', END: END},
    )
    workflow.add_edge('retrieve_supervisors', 'fill_template')
    workflow.add_edge('fill_template', 'final_answer')
    workflow.add_edge('final_answer', END)

    memory_saver = MemorySaver()

    recommendation_graph = workflow.compile(
        checkpointer=memory_saver
    )  # adding checkpointer, affects the way how "messages" field is built

    return recommendation_graph


if __name__ == '__main__':
    import asyncio

    graph = create_recommendation_workflow()
    thread_id = '1'

    while True:
        query = input('You: ')
        request_data = InputRecommendationGeneration(
            question=query, faculty='Faculty of Information and Communication Technology'
        )

        result = asyncio.run(run_graph(graph, request_data, thread_id))

        print('Chat: ' + result.as_str)
