import os
import sys
import pandas as pd

DATA_PATH = os.path.join("data", "raw", "smart_logistics_dataset.csv")

def main():
    if not os.path.exists(DATA_PATH):
        print(f"ERROR: dataset not found at {DATA_PATH}")
        print("Make sure smart_logistics_dataset.csv is inside data/raw/")
        sys.exit(1)

    # Read a small chunk first (safe for very large files)
    try:
        df = pd.read_csv(DATA_PATH, nrows=5000)  # read up to 5k rows for quick inspect
    except Exception as e:
        print("Failed to read CSV:", e)
        sys.exit(1)

    print("\n=== QUICK SUMMARY ===")
    print("Rows read (sample):", len(df))
    print("Columns:", len(df.columns))
    print("\n--- dtypes ---")
    print(df.dtypes)

    print("\n--- Missing values (per column) ---")
    print(df.isnull().sum().sort_values(ascending=False).head(20).to_string())

    print("\n--- Sample rows ---")
    print(df.head(5).to_string(index=False))

    print("\n--- Numeric summary ---")
    print(df.select_dtypes(include=["number"]).describe().transpose().to_string())

    # Show count of unique values for non-numeric-ish columns (top 10 columns)
    non_num = df.select_dtypes(exclude=["number"]).columns.tolist()
    if non_num:
        print("\n--- Unique counts for top non-numeric columns ---")
        for col in non_num[:10]:
            print(f"{col}: {df[col].nunique()} unique values (sample: {df[col].dropna().unique()[:5]})")

    print("\nInspection complete. If you want, we can run a full read and save a cleaned copy next.")

if __name__ == "__main__":
    main()
