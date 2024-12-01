import os
from langchain_community.document_loaders.csv_loader import CSVLoader
from langchain_text_splitters import CharacterTextSplitter
from langchain_community.vectorstores import FAISS


def get_retriever(vectorstore_path, embeddings):
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

    retriever = db.as_retriever(search_kwargs={"k": 8})
    return retriever
