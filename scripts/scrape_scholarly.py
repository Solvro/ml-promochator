from utils import scrape_to_csv

import fire


def main(staff_data_path: str = './data/staff_data', csv_path: str = './data/papers_data.csv'):
    scrape_to_csv(staff_data_path, csv_path)


if __name__ == '__main__':
    fire.Fire(main)
