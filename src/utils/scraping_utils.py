from scholarly import scholarly
from scholarly import ProxyGenerator
import csv
import json
import nltk
import unidecode
import string
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize


pg = ProxyGenerator()


def scrape_to_csv(authors_file_path: str, csv_path: str) -> None:
    _setup_nltk_resources()
    authors = []
    with open(authors_file_path, 'r', encoding='utf-8') as file:
        for line in file:
            name = line.strip()
            authors.append(str(name))

    csv_file = csv_path
    with open(csv_file, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["Supervisor's name", 'interests', 'research papers'])
        for author in authors:
            name, interests, research_papers = _scrape_author_data(author)
            writer.writerow(
                [
                    name,
                    ' '.join(interests),
                    json.dumps(research_papers),
                ]
            )


def _scrape_author_data(author_name: str) -> tuple[str, str, dict[str, str]]:
    search_query = scholarly.search_author(author_name)
    try:
        first_author_result = next(search_query)
    except StopIteration:
        return author_name, '', {}

    author_dict = scholarly.fill(first_author_result)
    name = author_dict['name']
    interests = author_dict['interests']

    papers = author_dict['publications'][:10]
    research_papers = {}
    papers_count = 0

    for paper in papers:
        paper_filled = scholarly.fill(paper)
        try:
            research_papers[paper_filled['bib']['title']] = _text_compression_pipeline(paper_filled['bib']['abstract'])
        except KeyError:
            continue
        papers_count += 1
        if papers_count == 5:
            break

    return name, interests, research_papers


def _text_compression_pipeline(text: str) -> str:
    stop_words = set(stopwords.words('english'))
    text = unidecode.unidecode(text.lower())
    words = word_tokenize(text)
    processed_text = [word for word in words if word.lower() not in stop_words and word not in string.punctuation]

    return ' '.join(processed_text)


def _setup_nltk_resources():
    try:
        nltk.data.find('corpora/stopwords')
    except LookupError:
        nltk.download('stopwords')

    try:
        nltk.data.find('tokenizers/punkt')
    except LookupError:
        nltk.download('punkt')
