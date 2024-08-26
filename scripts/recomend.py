from langchain_community.document_loaders.csv_loader import CSVLoader
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import CharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain_openai import OpenAI
import fire
import os
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


def main(
    question: str = "Who should I pick as promotor for my engineering thesis 'Train Rescheduling and Track Closure Optimization'",
):
    formatted_prompt = PROMPT_TEMPLATE.format(question=question)
    print(qa_chain.invoke(formatted_prompt)["result"])


if __name__ == "__main__":
    fire.Fire(main)