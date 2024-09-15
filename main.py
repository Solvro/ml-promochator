from fastapi import FastAPI
from pydantic import BaseModel

from dotenv import load_dotenv

from src.components.chains import qa_chain
from src.components.prompts import PROMPT_TEMPLATE

load_dotenv()


app = FastAPI()


class DetectionRequest(BaseModel):
    data: str


@app.post("/recommend")
async def recommend(data: DetectionRequest):
    formatted_prompt = PROMPT_TEMPLATE.format(question=data.data)
    output = qa_chain.invoke(formatted_prompt)["result"]

    response = {"response": output}

    return response


@app.get("/health")
async def health():
    return {"status": "Healthy"}
