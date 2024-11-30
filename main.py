from fastapi import FastAPI
from langserve import add_routes
from pydantic import BaseModel

from src.components.chains import qa_chain


app = FastAPI(
    title="LangChain Server",
    version="1.0",
    description="A simple api server using Langchain's Runnable interfaces",
)

add_routes(
    app,
    qa_chain,
    path="/recommend",
)
