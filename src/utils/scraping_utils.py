from scholarly import scholarly
from scholarly import ProxyGenerator
import csv
import json
import os
import nltk
import unidecode
import string
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
import pandas as pd
import PyPDF2


pg = ProxyGenerator()


FACULTIES = {
    "W1_": "Faculty of Architecture",
    "W2_": "Faculty of Civil Engineering",
    "W3_": "Faculty of Chemistry",
    "W4N": "Faculty of Information and Communication Technology",
    "W5_": "Faculty of Electrical Engineering",
    "W6_": "Faculty of Geoengineering, Mining and Geology",
    "W7_": "Faculty of Environmental Engineering",
    "W8N": "Faculty of Management",
    "W9_": "Faculty of Mechanical and Power Engineering",
    "W10": "Faculty of Mechanical Engineering",
    "W11": "Faculty of Fundamental Problems of Technology",
    "W12": "Faculty of Electronics, Photonics and Microsystems",
    "W13": "Faculty of Pure and Applied Mathematics",
    "W14": "Faculty of Medicine",
}


def scrape_to_csv(staff_data_path: str, csv_path: str) -> None:
    _setup_nltk_resources()

    csv_file = csv_path
    file_exists = os.path.isfile(csv_file)

    with open(csv_file, mode="a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(
                ["Supervisor's name", "faculty", "interests", "research papers"]
            )

        for json_file_name in os.listdir(staff_data_path):
            faculty = FACULTIES[json_file_name[:3]]
            json_file_path = os.path.join(staff_data_path, json_file_name)
            with open(json_file_path, "r", encoding="utf-8") as json_file:
                data = json.load(json_file)

                for author_data in data:
                    name = f"{author_data['first_name']} {author_data['last_name']}"
                    titles = author_data.get("titles", {}).get("before", "")
                    if (
                        titles != "mgr inż."
                        and titles != "mgr"
                        and titles != "mgr inż. arch."
                    ):
                        interests, research_papers = _scrape_author_data(name)

                        writer.writerow(
                            [
                                f"{titles} {name}",
                                faculty,
                                " ".join(interests),
                                json.dumps(research_papers),
                            ]
                        )


def add_apd_data(input_csv: str, output_csv: str, json_path: str, abstracts_path: str):
    _setup_nltk_resources()
    
    promotor_to_theses = _get_theses(json_path, abstracts_path)
    with open(input_csv, 'r', encoding='utf-8') as infile, open(output_csv, 'w', newline='', encoding='utf-8') as outfile:
        reader = csv.DictReader(infile)
        fieldnames = reader.fieldnames + ["Supervisor's Theses"]
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()

        for row in reader:
            supervisor_name = row["Supervisor's name"]
            theses = promotor_to_theses.get(supervisor_name, {})
            
            row["Supervisor's Theses"] = json.dumps(theses, ensure_ascii=False)
            
            writer.writerow(row)



def _scrape_author_data(author_name: str) -> tuple[str, str, dict[str, str]]:
    search_query = scholarly.search_author(author_name)
    try:
        first_author_result = next(search_query)
    except StopIteration:
        return "", {}

    author_dict = scholarly.fill(first_author_result)
    interests = author_dict["interests"]

    papers = author_dict["publications"][:10]
    research_papers = {}
    papers_count = 0

    for paper in papers:
        paper_filled = scholarly.fill(paper)
        try:
            research_papers[paper_filled["bib"]["title"]] = _text_compression_pipeline(
                paper_filled["bib"]["abstract"]
            )
        except KeyError:
            continue
        papers_count += 1
        if papers_count == 5:
            break

    return interests, research_papers


def _text_compression_pipeline(text: str) -> str:
    stop_words = set(stopwords.words("english"))
    text = unidecode.unidecode(text.lower())
    words = set(word_tokenize(text))
    processed_text = [
        word
        for word in words
        if word.lower() not in stop_words and word not in string.punctuation
    ]

    return " ".join(processed_text)


def _text_compression_pipeline_w_stemming(text: str) -> str:
    stop_words = set(stopwords.words("english"))
    stemmer = PorterStemmer()

    text = unidecode.unidecode(text.lower())
    words = word_tokenize(text)
    words = [stemmer.stem(word) for word in set(words)]
    processed_text = [
        word
        for word in words
        if word.lower() not in stop_words and word not in string.punctuation
    ]

    return " ".join(processed_text)

def _get_theses(json_path: str, abstracts_path: str):
    with open(json_path, 'r', encoding='utf-8') as json_file:
        thesis_data = json.load(json_file)

    promotor_to_theses = {}
    for thesis in thesis_data:
        try:
            promotor = thesis["thesis_promotor"]
        except KeyError:
            continue
        if promotor not in promotor_to_theses:
            promotor_to_theses[promotor] = {}
        if thesis["en_abstract"] != '' and not thesis["en_abstract"].startswith('http'):
            promotor_to_theses[promotor][thesis["en_title"]] = _text_compression_pipeline(thesis["en_abstract"])
        else:
            promotor_to_theses[promotor][thesis["en_title"]] = _read_pdf_abstract(f'{abstracts_path}/en/en_abstract_id_{thesis["thesis_id"]}.pdf')
    return promotor_to_theses

def _read_pdf_abstract(abstract_path: str):
    try:
        with open(abstract_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            text = ""
            for page_num in range(len(reader.pages)):
                page = reader.pages[page_num]
                text += page.extract_text()
            return _text_compression_pipeline(text)
    except:
        return ''

def _setup_nltk_resources():
    try:
        nltk.data.find("corpora/stopwords")
    except LookupError:
        nltk.download("stopwords")

    try:
        nltk.data.find("tokenizers/punkt")
    except LookupError:
        nltk.download("punkt")
