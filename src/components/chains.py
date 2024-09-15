from langchain.chains import RetrievalQA

from src.components.llms import llm
from src.components.database import get_retriever
from src.components.constants import VECTORSTORE_PATH
from src.components.embeddings import openai_embeddings


retriever = get_retriever(VECTORSTORE_PATH, openai_embeddings)
llm_ = llm.with_config(configurable={"llm":"openai"})

qa_chain = RetrievalQA.from_chain_type(
    llm=llm_,
    chain_type="stuff",
    retriever=retriever,
    return_source_documents=True,
)
