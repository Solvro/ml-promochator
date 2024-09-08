from fastapi import FastAPI
from pydantic import BaseModel

from langchain_openai import OpenAIEmbeddings
from langchain.chains import RetrievalQA
from langchain_openai import OpenAI
from dotenv import load_dotenv

from src.constants import PROMPT_TEMPLATE, VECTORSTORE_PATH
from src.database import get_retriever

load_dotenv()

embeddings = OpenAIEmbeddings()


retriever = get_retriever(VECTORSTORE_PATH, embeddings)


qa_chain = RetrievalQA.from_chain_type(
    llm=OpenAI(temperature=0.2),
    chain_type="stuff",
    retriever=retriever,
    return_source_documents=True,
)


app = FastAPI()


class DetectionRequest(BaseModel):
    data: str


@app.post("/detect")
async def detect(data: DetectionRequest):
    """
    Endpoint to process plain text input.

    Args:
        data (str): The plain text data sent in the POST request.

    Returns:
        dict: A dictionary with the original data and a message.
    """
    formatted_prompt = PROMPT_TEMPLATE.format(question=data.data)
    output = qa_chain.invoke(formatted_prompt)["result"]

    response = {"response": output}

    return response


@app.get("/health")
async def health():
    """
    Health check endpoint to ensure the API is running.

    Returns:
        dict: A simple dictionary with a status message.
    """
    return {"status": "Healthy"}
