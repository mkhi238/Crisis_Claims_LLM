import unicodedata, re

def normalize_text(s):
    s = unicodedata.normalize("NFKC", str(s)).strip().lower()
    s = re.sub(r"\s+", " ", s)
    return s

def clean_data(dataset, split_name, canon = None, text_col = "claim", label_col = "label", id_col = "id"):
    df = dataset.to_pandas() if hasattr(dataset, "to_pandas") else dataset.copy()
    rename = {text_col: "claim", label_col: "label"}
    if id_col in df.columns:
        rename[id_col] = "id"
    df = df.rename(columns = rename)
    df['claim'] = df['claim'].apply(normalize_text)
    if canon:
        df['label'] = df['label'].astype(str).str.lower().map(canon)
    df = df.dropna(subset = ['claim', 'label']).copy()
    df['split'] = split_name
    return df

