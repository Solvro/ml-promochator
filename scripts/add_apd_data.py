from utils import add_apd_data

import fire


def main(
        input_csv: str = "./data/papers_data.csv", output_csv: str = "./data/papers_data_2.csv", 
        json_path: str = "./data/theses_data.json", abstracts_path: str = "./data/pdf_abstracts"
):
    add_apd_data(input_csv, output_csv, json_path, abstracts_path)


if __name__ == "__main__":
    fire.Fire(main)