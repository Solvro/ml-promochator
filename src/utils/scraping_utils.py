from scholarly import scholarly
from scholarly import ProxyGenerator
import csv
import json

pg = ProxyGenerator()


def save_data_to_csv(authors_file: str, csv_path: str) -> None:
    authors = []
    with open(authors_file, 'r', encoding='utf-8') as file:
        for line in file:
            name = line.strip()
            authors.append(str(name))

    csv_file = csv_path
    with open(csv_file, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["Supervisor's name", 'interests', 'research papers'])
        for author in authors:
            name, interests, research_papers = _scrape_data(author)
            writer.writerow(
                [
                    name,
                    ' '.join(interests),
                    json.dumps(research_papers),
                ]
            )


def _scrape_data(author_name: str) -> tuple[str, str, dict[str, str]]:
    search_query = scholarly.search_author(author_name)
    first_author_result = next(search_query)
    author_dict = scholarly.fill(first_author_result)
    name = author_dict['name']
    interests = author_dict['interests']
    publications = author_dict['publications'][:5]
    research_papers = {}

    for pub in publications:
        pub_filled = scholarly.fill(pub)
        research_papers[pub_filled['bib']['title']] = pub_filled['bib']['abstract']

    return name, interests, research_papers
