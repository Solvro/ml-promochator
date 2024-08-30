import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from langchain_community.document_loaders.csv_loader import CSVLoader
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import CharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain_openai import OpenAI
from dotenv import load_dotenv


load_dotenv()

vectorstore_path = "./vectorstores/test_vectorstore"
embeddings = OpenAIEmbeddings()

if os.path.exists(vectorstore_path):
    db = FAISS.load_local(
        vectorstore_path, embeddings, allow_dangerous_deserialization=True
    )
else:
    loader = CSVLoader(file_path="./data/authors_with_papers.csv", encoding="utf-8")
    data = loader.load()

    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
    documents = text_splitter.split_documents(data)

    db = FAISS.from_documents(documents, embeddings)
    db.save_local(vectorstore_path)


retriever = db.as_retriever(search_kwargs={"k": 5})

qa_chain = RetrievalQA.from_chain_type(
    llm=OpenAI(temperature=0.2),
    chain_type="stuff",
    retriever=retriever,
    return_source_documents=True,
)

PROMPT_TEMPLATE = """
You are an expert in providing information about thesis supervisors at Politechnika Wrocławska.
When given a user question about the most suitable thesis supervisors for their project based on their reasearch papers and intrests, provide 3 supervisor's and their' faculty along with titles of some of their research papers.

User Question:
{question}

Response:
"""

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
