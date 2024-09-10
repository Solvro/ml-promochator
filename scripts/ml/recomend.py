from langchain_openai import OpenAIEmbeddings
from langchain.chains import RetrievalQA
from langchain_openai import OpenAI
import fire
import os
from dotenv import load_dotenv

from app.core.config import PROMPT_TEMPLATE, VECTORSTORE_PATH
from app.core.database import get_retriever


load_dotenv()

embeddings = OpenAIEmbeddings()

retriever = get_retriever(VECTORSTORE_PATH, embeddings)

qa_chain = RetrievalQA.from_chain_type(
    llm=OpenAI(temperature=0.2),
    chain_type="stuff",
    retriever=retriever,
    return_source_documents=True,
)


def main(
    question: str = "Who should I pick as supervisor for my thesis 'Train Rescheduling and Track Closure Optimization'",
):
    formatted_prompt = PROMPT_TEMPLATE.format(question=question)
    print(qa_chain.invoke(formatted_prompt)["result"])


if __name__ == "__main__":
    fire.Fire(main)
