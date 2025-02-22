import fire
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains.retrieval import create_retrieval_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI, OpenAIEmbeddings

from src.components.constants import VECTORSTORE_PATH
from src.components.database import get_vectorstore
from src.components.prompts import PROMPT_TEMPLATE

embeddings = OpenAIEmbeddings()

retriever = get_vectorstore(VECTORSTORE_PATH, embeddings).as_retriever(search_kwargs={'k': 2})

llm = ChatOpenAI(temperature=0.2, model='gpt-4o-mini', max_tokens=2560)
prompt = ChatPromptTemplate.from_template(
    PROMPT_TEMPLATE,
)

question_answer_chain = create_stuff_documents_chain(llm, prompt)
qa_chain = create_retrieval_chain(retriever, question_answer_chain)

# qa_chain = RetrievalQA.from_chain_type(
#     llm=OpenAI(temperature=0.2),
#     chain_type="stuff",
#     retriever=retriever,
#     return_source_documents=True,
# )


def main(
    question: str = "Who should I pick as supervisor for my thesis 'Deep generative neural networks'",
):
    print(qa_chain.invoke({'input': question})['answer'])


if __name__ == '__main__':
    fire.Fire(main)
