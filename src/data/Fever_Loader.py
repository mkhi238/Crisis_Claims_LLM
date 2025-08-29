from datasets import load_dataset
import pandas as pd
from pathlib import Path
import unicodedata, re

canon = {'supports': 'SUPPORTS', 
         'refutes': 'REFUTES',
         'not enough info': 'NOT ENOUGH INFO',
         'nei': 'NOT ENOUGH INFO'}

def remove_duplicates(dataset):
    df = dataset.to_pandas()
    df = df.drop_duplicates(subset = ['id', 'claim' , 'label'], keep = "first")
    return df.loc[:,['id', 'label', 'claim']]

def normalize_text(s):
    s = unicodedata.normalize("NFKC", str(s)).strip().lower()
    s = re.sub(r"\s+", " ", s)
    return s

def clean_data(dataset, split_name):
    dataset = remove_duplicates(dataset)
    dataset['claim'] = dataset['claim'].apply(normalize_text)
    dataset['label'] = dataset['label'].astype(str).str.lower().map(canon)
    dataset = dataset.dropna(subset = ['claim', 'label'])
    dataset['split'] = split_name
    return dataset

def main():
    dataset = load_dataset("fever", "v1.0")
    train = clean_data(dataset['train'], 'train')
    valid = clean_data(dataset['labelled_dev'], 'valid')
    test = clean_data(dataset['paper_test'], 'test')
    df = pd.concat([train, valid, test], ignore_index=True)
    priority = {'train': 0, 'valid': 1, 'test': 2}
    df['prio'] = df['split'].map(priority)
    df = df.sort_values(['claim', 'prio'])
    df = df.drop_duplicates(subset=["claim_clean"], keep="first")
    df = df.drop('prio', axis = 1).reset_index(drop = True)

    


if __name__ == "__main__":
    main()

