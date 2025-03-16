from src.components.llms import chat_llm
from src.components.database import get_vectorstore
from src.components.constants import VECTORSTORE_PATH
from src.components.embeddings import openai_embeddings
from src.components.prompts import PROMPT_TEMPLATE, SYSTEM_PROMPT
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.documents import Document


template = ChatPromptTemplate(
    [
        ('system', SYSTEM_PROMPT),
        ('human', PROMPT_TEMPLATE),
    ]
)

vectorstore = get_vectorstore(VECTORSTORE_PATH, openai_embeddings)

retriever = vectorstore.as_retriever(search_kwargs={'k': 8})

def _format_docs(docs: list[Document]) -> str:
    """
    Formats documents by joining their content into a single string.

    Parameters:
        docs (list[Document]): List of documents returned by the retriever
    Returns:
        str (str): Concatenated text of documents separated by three new lines
    """
    return "\n\n\n".join([d.page_content for d in docs])

qa_chain = (
    {"retrieved_context": retriever | _format_docs, "question": RunnablePassthrough()}
    | template
    | chat_llm
)


if __name__ == '__main__':
    recom = qa_chain.invoke('Deep Generative Models')
    print(recom)
    print(recom.as_str)
