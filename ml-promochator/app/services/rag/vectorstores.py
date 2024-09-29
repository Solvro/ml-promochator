from typing import List

from langchain_core.embeddings.embeddings import Embeddings
from langchain.schema import Document
from langchain.vectorstores.pgvector import PGVector
from sqlmodel import Session, select

from app.core.config import settings
from app.models import Supervisor, TextChunk
from app.services.rag.loaders import CSVLoaderWithSplitter


class VectorStore:
    def __init__(self, session: Session, embedding_function: Embeddings):
        self.session = session
        self.embedding_function = embedding_function
        self.vectorstore = PGVector(
            connection_string = settings.SQLALCHEMY_DATABASE_URI,
            embedding_function = embedding_function,
            collection_name = "supervisors"
        )
    
    def add_documents(self, documents: List[Document]):
        self.vectorstore.add_documents(documents)
    
    def search(self, query_embedding: List[float], k: int = 5) -> List[Document]:
        return self.vector_store.similarity_search(query_embedding, k=k)


def generate_embeddings(documents: List[Document], embedding_function: Embeddings) -> List[List[float]]:
    embedding_model = embedding_function
    embeddings = [embedding_model.embed(doc.page_content) for doc in documents]
    return embeddings


def store_data_in_db(documents: List[Document], embeddings: List[List[float]], session: Session) -> None:
    for i, doc in enumerate(documents):
        metadata = doc.metadata
        chunk_content = doc.page_content

        supervisor = session.exec(select(Supervisor).where(Supervisor.full_name == metadata["full_name"])).first()
        if not supervisor:
            supervisor = Supervisor(
                full_name=metadata["full_name"],
                faculty=metadata["faculty"],
                research_papers=metadata["research_papers"],
                supervised_papers=metadata["supervised_papers"]
            )
            session.add(supervisor)
            session.commit()
            session.refresh()

        chunk = TextChunk(
            page_content=chunk_content,
            embedding=embeddings[i],
            supervisor_id=supervisor.id
        )
        session.add(chunk)
    session.commit()


def init_db_with_csv(filepath: str, session: Session) -> None:
    loader_with_splitter = CSVLoaderWithSplitter(filepath,
                                                 settings.CHUNKS_SIZE,
                                                 settings.CHUNKS_OVERLAP)
    documents = loader_with_splitter.load_and_split()
    embeddings = generate_embeddings(documents)
    store_data_in_db(documents, embeddings, session)