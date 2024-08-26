import pandas as pd

def count_no_papers(file_path: str='../data/papers_data.csv'):
    df = pd.read_csv(file_path)
    return df['research papers'].astype(str).apply(lambda x: x.count('{}')).sum()