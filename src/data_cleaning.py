import os
import pandas as pd

RAW_PATH = os.path.join("data", "raw", "smart_logistics_dataset.csv")
PROCESSED_PATH = os.path.join("data", "processed", "cleaned_logistics_data.csv")

def main():
    if not os.path.exists(RAW_PATH):
        print(f"Dataset not found at {RAW_PATH}")
        return

    df = pd.read_csv(RAW_PATH)

    # --- Step 1: Handle missing values ---
    # Fill missing 'Logistics_Delay_Reason' with 'Unknown'
    df['Logistics_Delay_Reason'] = df['Logistics_Delay_Reason'].fillna('Unknown')

    # --- Step 2: Convert Timestamp to datetime ---
    df['Timestamp'] = pd.to_datetime(df['Timestamp'], errors='coerce')

    # --- Step 3: Handle any corrupted timestamps ---
    df = df.dropna(subset=['Timestamp'])

    # --- Step 4: Remove obvious duplicates ---
    df = df.drop_duplicates()

    # --- Step 5: Save cleaned data ---
    os.makedirs(os.path.dirname(PROCESSED_PATH), exist_ok=True)
    df.to_csv(PROCESSED_PATH, index=False)

    print(f"Cleaned data saved to: {PROCESSED_PATH}")
    print(f"Rows after cleaning: {len(df)} | Columns: {len(df.columns)}")
    print("Sample rows after cleaning:")
    print(df.head(5).to_string(index=False))

if __name__ == "__main__":
    main()
