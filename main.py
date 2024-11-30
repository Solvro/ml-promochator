from fastapi import FastAPI
from langserve import add_routes
from pydantic import BaseModel

from src.components.chains import qa_chain


# app = FastAPI()


# class DetectionRequest(BaseModel):
#     data: str


# @app.post("/recommend")
# async def recommend(data: DetectionRequest):
#     formatted_prompt = PROMPT_TEMPLATE.format(question=data.data)
#     output = qa_chain.invoke(formatted_prompt)["result"]

#     response = {"response": output}

#     return response


# @app.get("/health")
# async def health():
#     return {"status": "Healthy"}

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
