import csv

from langchain_core.documents import Document


def load_csv(file_path: str) -> list[Document]:
    """
    Loads supervisor data from a CSV file and converts each row into a Document object.

    Parameters:
        file_path (str): Path to the CSV file containing supervisor information.
    Returns:
        docs (list[Document]): List of Document objects containing supervisor details.
    """
    docs = []
    with open(file_path, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            page_content = (
                f'{row["Supervisors name"]}, {row["faculty"]}:'
                + '\n\n'
                + f'research papers: {row["research papers"]}'
                + '\n\n'
                + f'theses: {row["Supervisors Theses"]}'
            )
            doc = Document(
                page_content=page_content,
                metadata={
                    "Supervisor's name": row['Supervisors name'],
                    'faculty': row['faculty'],
                },
            )
            docs.append(doc)
    return docs
