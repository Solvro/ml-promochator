from typing import List

from langchain.document_loaders import CSVLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.schema import Document


class CSVLoaderWithSplitter:
    def __init__(self, filepath: str, chunk_size: int = 1000, chunk_overlap: int = 0):
        self.file_path = filepath
        self.text_splitter = CharacterTextSplitter(
            separator=" ",
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap
        )

    def load_and_split(self) -> List[Document]:
        loader = CSVLoader(self.file_path)
        documents = loader.load()

        split_documents = []
        for doc in documents:
            chunks = self.text_splitter.split_text(doc.page_content)
            for chunk in chunks:
                split_doc = Document(page_content=chunk, metadata=doc.metadata)
                split_documents.append(split_doc)

        return split_documents
