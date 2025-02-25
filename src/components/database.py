import os
import time
from uuid import uuid4
from langchain_community.docstore.in_memory import InMemoryDocstore
from langchain_community.vectorstores import FAISS
import faiss
from src.components.loaders import load_csv


def get_vectorstore(vectorstore_path, embeddings):
    """
    Loads or creates a FAISS-based vector store for document retrieval.
    
    If a vector store exists at the given path, it loads the stored index. Otherwise, it creates
    a new FAISS index, processes supervisor data from a CSV file, and adds them to the database.
    
    Parameters:
        vectorstore_path: Path to the stored FAISS database.
        embeddings: Embedding model used to generate vector representations of documents.
    Returns:
        db: A FAISS vector store instance.
    """
    if os.path.exists(vectorstore_path):
        db = FAISS.load_local(
            vectorstore_path, embeddings, allow_dangerous_deserialization=True
        )
    else:
        index = faiss.IndexFlatL2(len(embeddings.embed_query("hello world")))
        db = FAISS(
            embedding_function=embeddings,
            index=index,
            docstore=InMemoryDocstore(),
            index_to_docstore_id={},
        )

        documents = load_csv("./data/supervisors_data.csv")
        uuids = [str(uuid4()) for _ in range(len(documents))]

        batch_size = 600
        total_batches = (len(documents) + batch_size - 1) // batch_size

        # Vectorize data in batches because of openai token limit TPM (token per minute)
        for batch_idx in range(total_batches):
            start_idx = batch_idx * batch_size
            end_idx = min(start_idx + batch_size, len(documents))
            batch_docs = documents[start_idx:end_idx]
            batch_uuids = uuids[start_idx:end_idx]

            print(
                f"Adding batch {batch_idx + 1}/{total_batches} ({len(batch_docs)} documents)..."
            )
            db.add_documents(documents=batch_docs, ids=batch_uuids)

            if batch_idx < total_batches - 1:
                print("Pausing for 1 minute...")
                time.sleep(60)

        db.save_local(vectorstore_path)
    return db


if __name__ == "__main__":
    from src.components.constants import VECTORSTORE_PATH
    from src.components.embeddings import openai_embeddings

    get_vectorstore(VECTORSTORE_PATH, openai_embeddings)
