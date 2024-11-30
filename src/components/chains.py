from src.components.llms import chat_llm
from src.components.database import get_retriever
from src.components.constants import VECTORSTORE_PATH
from src.components.embeddings import openai_embeddings
from src.components.prompts import PROMPT_TEMPLATE

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough


prompt = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
retriever = get_retriever(VECTORSTORE_PATH, openai_embeddings)


def format_docs(docs):
    return "\n\n".join([d.page_content for d in docs])


qa_chain = (
    {"retrieved_context": retriever | format_docs, "question": RunnablePassthrough()}
    | prompt
    | chat_llm
)


if __name__ == "__main__":
    recom = qa_chain.invoke("Deep Generative Models")
    print(recom)
    print(recom.as_str)
