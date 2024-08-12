from langchain_community.document_loaders.csv_loader import CSVLoader
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import CharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain_openai import OpenAI
import fire


loader = CSVLoader(file_path='./data/papers_data.csv')
data = loader.load()


text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
documents = text_splitter.split_documents(data)
db = FAISS.from_documents(documents, OpenAIEmbeddings())

retriever = db.as_retriever(search_kwargs={'k': 5})

qa_chain = RetrievalQA.from_chain_type(
    llm=OpenAI(temperature=0.2),
    chain_type='stuff',
    retriever=retriever,
    return_source_documents=True,
)

PROMPT_TEMPLATE = """
You are an expert in providing information about thesis supervisors at Politechnika Wrocławska.
When given a user question about the most suitable thesis supervisor for their project based on their reasearch papers and intrests, provide the supervisor's name along with titles of their research papers.

User Question:
{question}

Response:
"""


def main(
    question: str = "Who should I pick as promotor for my engineering thesis 'Train Rescheduling and Track Closure Optimization'",
):
    formatted_prompt = PROMPT_TEMPLATE.format(question=question)
    print(qa_chain.invoke(formatted_prompt)['result'])


if __name__ == '__main__':
    fire.Fire(main)
