import pandas as pd
from pathlib import Path
from common import normalize_text 


def main():

  df = pd.read_csv("C:\Users\mukun\crisis-claim-analysis\data\processed\fever_cleaned.csv")

  df = df[df[""]]