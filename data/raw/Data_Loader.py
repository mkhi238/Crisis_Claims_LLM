import pandas as pd
from datasets import load_dataset
from sklearn.model_selection import train_test_split

def load_fever(save_dir=r"C:\Users\mukun\crisis-claim-analysis\data\raw"):
    save_path = Path(save_dir)
    save_path.mkdir(parents=True, exist_ok=True)

    dataset = load_dataset("fever", "v1.0")

    for split in dataset.keys():
        out_file = save_path / f"fever_{split}.csv"
        dataset[split].to_csv(out_file, index=False)
        print(f"Saved {split} split to {out_file}")

    return dataset
fever = load_fever()



print(fever['train'][0])




if __name__ == "__main__":
    fever = load_fever()
    # Example: show first claim
    print(fever["train"][0])
