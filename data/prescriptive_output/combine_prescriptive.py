import os
import pandas as pd

# ---------------- CONFIGURATION ----------------
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
INPUT_DIR = os.path.join(BASE_DIR, "data", "prescriptive_output")
OUTPUT_FILE = os.path.join(INPUT_DIR, "master_prescriptive_summary.csv")

# Keywords that mean "not a main summary file"
EXCLUDE_KEYWORDS = ["details", "summary", "asset_summary", "cost_summary", "temp_summary", "humidity_summary"]

# ------------------------------------------------
def is_main_summary(filename: str) -> bool:
    """Return True if filename looks like a main summary file."""
    lower = filename.lower()
    if not lower.endswith(".csv"):
        return False
    if any(key in lower for key in EXCLUDE_KEYWORDS):
        return False
    if "optimization_results" not in lower:
        return False
    return True

def extract_module_name(filename: str) -> str:
    """Extract module name like traffic, waiting_time, etc."""
    return filename.replace("_optimization_results.csv", "").replace(".csv", "").title().replace("_", " ")

def combine_prescriptive_files():
    all_files = [f for f in os.listdir(INPUT_DIR) if is_main_summary(f)]

    if not all_files:
        print(" No prescriptive summary CSV files found in:", INPUT_DIR)
        return

    combined_df = pd.DataFrame()

    for file in all_files:
        path = os.path.join(INPUT_DIR, file)
        module_name = extract_module_name(file)
        try:
            df = pd.read_csv(path)
            df["Module_Name"] = module_name
            combined_df = pd.concat([combined_df, df], ignore_index=True)
            print(f" Added: {file} ({len(df)} rows)")
        except Exception as e:
            print(f" Error reading {file}: {e}")

    # Save combined result
    combined_df.to_csv(OUTPUT_FILE, index=False)
    print(f"\n Combined {len(all_files)} main result files into:")
    print(f"➡ {OUTPUT_FILE}")
    print(f" Total rows combined: {len(combined_df)}")

def main():
    print("\n Starting Master Prescriptive Summary Combination...\n")
    combine_prescriptive_files()
    print("\n Combination complete. File ready for Power BI.\n")

if __name__ == "__main__":
    main()
