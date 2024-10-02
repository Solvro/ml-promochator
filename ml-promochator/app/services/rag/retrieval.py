from langchain.chains import RetrievalQA
from langchain_core.language_models.llms import BaseLLM
from langchain_openai import OpenAIEmbeddings

from app.api.deps import SessionDep
from app.core.config import settings
from app.services.rag.models import get_model
from app.services.rag.prompt import Prompt
from app.services.rag.vectorstores import VectorStore


class RAGSystem:
    def __init__(self, vector_store: VectorStore, model: BaseLLM, template: str):
        self.vector_store = vector_store
        self.llm = model
        self.template = template

        self.qa_chain = RetrievalQA.from_chain_type(
            llm=self.llm,
            chain_type="stuff",
            retriever=self.vector_store.retrevier,
            return_source_documents=True,
        )

    def answer_query(self, query: str) -> dict:
        prompt = Prompt(self.template, query)
        response = self.qa_chain.invoke(prompt)["result"]
        return response


def recommend_supervisor(
    text: str,
    session: SessionDep
) -> str:
    vectorstore = VectorStore(session,
                              OpenAIEmbeddings)
    rag_system = RAGSystem(vectorstore,
                           get_model(),
                           settings.PROMPT_TEMPLATE_FILE)

    answer = rag_system.answer_query(text)
    return answer