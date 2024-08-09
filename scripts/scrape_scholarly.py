import sys

sys.path.append('.')
from src.utils import scrape_to_csv

import fire


def main(authors_file_path: str = './data/pwr_authors.txt', csv_path: str = './data/papers_data.csv'):
    scrape_to_csv(authors_file_path, csv_path)


if __name__ == '__main__':
    fire.Fire(main)
