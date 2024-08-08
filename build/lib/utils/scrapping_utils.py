from scholarly import scholarly
from scholarly import ProxyGenerator
import csv
import json
import os


def save_data_to_csv(self, authors: list[str]) -> None:
    csv_file = self.file_path
    with open(csv_file, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["Supervisor's name", 'interests', 'research papers'])
        for author in authors:
            name, interests, research_papers = _get_author_data(author)
            writer.writerow(
                [
                    name,
                    interests,
                    research_papers,
                ]
            )


def _get_author_data(author_name: str) -> tuple[str, str, dict[str, str]]:
    search_query = scholarly.search_author(author_name)
    first_author_result = next(search_query)
    author_dict = scholarly.fill(first_author_result)
    name = author_dict['name']
    interests = author_dict['interests']
    publications = author_dict['publications'][:5]
    research_papers = {}
    for pub in publications:
        research_papers[pub['bib']['title']] = pub['bib']['abstract']

    return name, interests, research_papers
