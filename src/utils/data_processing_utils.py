import pandas as pd


def split_csv_by_empty_papers(
    output_file_not_empty: str, output_file_empty: str
) -> None:
    df = pd.read_csv("../data/papers_data.csv")

    df_no_papers = df[df["research papers"] == "{}"]
    df_papers = df[df["research papers"] != "{}"]

    df_papers.to_csv(output_file_not_empty, index=False)
    df_no_papers.to_csv(output_file_empty, index=False)


# Remove rows where both columns are equal to '{}'
def clean_csv(file_path):
    df = pd.read_csv(file_path)

    df_cleaned = df[
        ~((df["research papers"] == "{}") & (df["Supervisor's Theses"] == "{}"))
    ]

    df_cleaned.to_csv(file_path, index=False)
