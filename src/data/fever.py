from datasets import load_dataset
import pandas as pd
from common import clean_data

canon = {'supports': 'TRUE', 
         'refutes': 'FALSE',
         'not enough info': 'NOT ENOUGH INFO',
         'nei': 'NOT ENOUGH INFO'}

def main():
    dataset = load_dataset("fever", "v1.0")
    train = clean_data(dataset['train'], 'train', canon, 'claim', 'label', 'id')
    validation = clean_data(dataset['labelled_dev'], 'valid', canon, 'claim', 'label', 'id')
    test = clean_data(dataset['paper_test'], 'test', canon, 'claim', 'label', 'id')
    df = pd.concat([train, validation, test], ignore_index=True)
    priority = {'train': 0, 'validation': 1, 'test': 2}
    df['prio'] = df['split'].map(priority)
    df = df.sort_values(['claim', 'prio'])
    df = df.drop_duplicates(subset=["claim"], keep="first")
    df = df.drop('prio', axis = 1).reset_index(drop = True)
    df.rename(columns={'label': 'label_map'}, inplace = True)
    label_map = {'TRUE': 0, 'FALSE': 1
    }
    df['labels'] = df['label_map'].map(label_map)
    df.rename(columns={'label_map' : 'label_text'}, inplace=True)
    df = df[['claim', 'label_text', 'labels', 'evidence_sentence_id', 'evidence_annotation_id', 'evidence_wiki_url']]
    df.to_csv("fever_cleaned.csv", index=False)
    
if __name__ == "__main__":
    main()

