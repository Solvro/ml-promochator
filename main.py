from fastapi import FastAPI
from langserve import add_routes
from langchain_core.runnables.utils import Output

from src.graph import recommendation_graph
from src.components.models import InputRecommendationGeneration


app = FastAPI(
    title="PromoCHATor",
    version="1.0",
    description="An api for recommending supervisors for thesis",
)

add_routes(
    app,
    recommendation_graph.with_types(
        input_type=InputRecommendationGeneration, output_type=Output
    ),
    path="/recommend",
)
