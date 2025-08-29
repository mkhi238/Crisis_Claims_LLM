from datasets import load_dataset
import pandas as pd
from pathlib import Path

wiki_dataset = load_dataset("fever", "wiki_pages", split="wikipedia_pages")

df = pd.DataFrame(wiki_dataset)
print(df.head())