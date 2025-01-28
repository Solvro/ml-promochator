import csv

from langchain_core.documents import Document


def load_csv(file_path):
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
