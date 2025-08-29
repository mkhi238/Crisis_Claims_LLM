from datasets import load_dataset
import pandas as pd
from pathlib import Path
import unicodedata, re
from common import remove_duplicates, normalize_text, clean_data

canon = {'supports': 'SUPPORTS', 
         'refutes': 'REFUTES',
         'not enough info': 'NOT ENOUGH INFO',
         'nei': 'NOT ENOUGH INFO'}

def main():
    dataset = load_dataset("fever", "v1.0")
    train = clean_data(dataset['train'], 'train', canon)
    valid = clean_data(dataset['labelled_dev'], 'valid', canon)
    test = dataset['paper_test']
    df = pd.concat([train, valid, test], ignore_index=True)
    priority = {'train': 0, 'validation': 1, 'test': 2}
    df['prio'] = df['split'].map(priority)
    df = df.sort_values(['claim', 'prio'])
    df = df.drop_duplicates(subset=["claim"], keep="first")
    df = df.drop('prio', axis = 1).reset_index(drop = True)
    df = df[df['label'] != 'NOT ENOUGH INFO']
    df.rename(columns={'label': 'label_map'}, inplace = True)
    label_map = {'SUPPORTS': 0, 'REFUTES': 1
    }
    df['label'] = df['label_map'].map(label_map)
    
if __name__ == "__main__":
    main()

