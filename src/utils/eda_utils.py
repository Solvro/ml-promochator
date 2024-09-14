import pandas as pd

def count_no_papers(file_path: str = "../data/papers_data_2.csv"):
    df = pd.read_csv(file_path)
    return df["research papers"].astype(str).apply(lambda x: x.count("{}")).sum()

def count_no_theses(file_path: str = "../data/papers_data_2.csv"):
    df = pd.read_csv(file_path)
    return df["Supervisor\'s Theses"].astype(str).apply(lambda x: x.count("{}")).sum()

def count_no_papers_n_theses(file_path: str = "../data/papers_data_2.csv") -> int:
    df = pd.read_csv(file_path)
    
    no_papers_count = df[
        (df["research papers"].astype(str) == '{}') &
        (df["Supervisor\'s Theses"].astype(str) == '{}')
    ].shape[0]
    
    return no_papers_count
