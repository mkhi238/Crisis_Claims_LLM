from datasets import load_dataset
import pandas as pd
from pathlib import Path
import unicodedata, re

def remove_duplicates(dataset):
    df = dataset.to_pandas()
    df = df.drop_duplicates(subset = ['id', 'claim' , 'label'], keep = "first")
    return df.loc[:,['id', 'label', 'claim']]

def normalize_text(s):
    s = unicodedata.normalize("NFKC", str(s)).strip().lower()
    s = re.sub(r"\s+", " ", s)
    return s

def clean_data(dataset, split_name, canon = None):
    dataset = remove_duplicates(dataset)
    dataset['claim'] = dataset['claim'].apply(normalize_text)
    dataset['label'] = dataset['label'].astype(str).str.lower().map(canon)
    dataset = dataset.dropna(subset = ['claim', 'label'])
    dataset['split'] = split_name
    return dataset