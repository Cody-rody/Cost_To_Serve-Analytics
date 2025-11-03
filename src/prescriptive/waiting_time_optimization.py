# src/prescriptive/waiting_time_optimization.py
"""
Prescriptive Module: Waiting Time Optimization
----------------------------------------------
Analyzes how waiting time contributes to delay penalties and prescribes
optimal waiting thresholds and cost-saving strategies.
"""

import pandas as pd
import numpy as np
import os

# -----------------------------
#  PATH CONFIGURATION
# -----------------------------
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
DATA_PATH = os.path.join(BASE_DIR, "data", "processed", "asset_utilization_cost.csv")
OUTPUT_PATH = os.path.join(BASE_DIR, "data", "processed", "waiting_time_optimization_results.csv")

# -----------------------------
#  LOAD DATA
# -----------------------------
def load_data():
    """Load the processed logistics dataset."""
    if not os.path.exists(DATA_PATH):
        raise FileNotFoundError(f"File not found: {DATA_PATH}")
    
    df = pd.read_csv(DATA_PATH)
    print(f"Data loaded successfully — {df.shape[0]} records, {df.shape[1]} columns.")
    return df

# -----------------------------
#  PREPROCESS
# -----------------------------
def preprocess(df):
    """Prepare data for analysis."""
    # Ensure waiting and penalty columns exist
    if "Waiting_Time" not in df.columns or "delay_penalty" not in df.columns:
        raise KeyError("Expected columns 'Waiting_Time' and 'delay_penalty' not found.")
    
    df["Waiting_Time"] = pd.to_numeric(df["Waiting_Time"], errors="coerce").fillna(0)
    df["delay_penalty"] = pd.to_numeric(df["delay_penalty"], errors="coerce").fillna(0)
    
    # Create bins for easier analysis
    bins = [0, 10, 20, 30, 40, 50, 60, np.inf]
    labels = ["0–10", "10–20", "20–30", "30–40", "40–50", "50–60", "60+"]
    df["waiting_bin"] = pd.cut(df["Waiting_Time"], bins=bins, labels=labels, include_lowest=True)
    return df

# -----------------------------
#  ANALYSIS
# -----------------------------
def analyze_waiting_cost(df, min_trips_threshold=5):
    """Analyze penalty vs waiting time to find optimal thresholds."""
    summary = (
        df.groupby("waiting_bin")
        .agg(
            avg_penalty=("delay_penalty", "mean"),
            total_penalty=("delay_penalty", "sum"),
            trips=("Asset_ID", "count")
        )
        .reset_index()
    )

    # Remove bins with too few trips (noise)
    summary = summary[summary["trips"] >= min_trips_threshold]

    if summary.empty:
        print(" Not enough valid data for meaningful recommendations.")
        return pd.DataFrame()

    # Identify bin with lowest avg penalty (cost sweet spot)
    optimal_bin = summary.loc[summary["avg_penalty"].idxmin()]

    # Calculate potential savings if waiting time is reduced to that bin
    current_avg = (df["delay_penalty"].mean())
    optimal_avg = optimal_bin["avg_penalty"]
    potential_saving = current_avg - optimal_avg

    # Prepare recommendations
    recommendations = pd.DataFrame({
        "Optimal_Waiting_Range": [optimal_bin["waiting_bin"]],
        "Min_Avg_Penalty": [round(optimal_bin["avg_penalty"], 2)],
        "Current_Avg_Penalty": [round(current_avg, 2)],
        "Estimated_Savings_Per_Trip": [round(potential_saving, 2)],
        "Trips_Analyzed": [int(optimal_bin["trips"])]
    })

    return recommendations, summary

# -----------------------------
#  SAVE RESULTS
# -----------------------------
def save_results(recommendations, summary):
    """Save results to CSV instead of Excel."""
    recommendations.to_csv(OUTPUT_PATH, index=False)
    summary_path = OUTPUT_PATH.replace(".csv", "_details.csv")
    summary.to_csv(summary_path, index=False)
    
    print(f" Results saved to:")
    print(f"   - {OUTPUT_PATH}")
    print(f"   - {summary_path}")


# -----------------------------
#  MAIN
# -----------------------------
def main():
    print("\nStarting Waiting Time Optimization Analysis...\n")

    df = load_data()
    df = preprocess(df)
    recommendations, summary = analyze_waiting_cost(df)

    if recommendations.empty:
        print(" No valid recommendations generated.")
    else:
        save_results(recommendations, summary)
        print("\nRecommended Waiting Time Range to Minimize Cost:\n")
        print(recommendations.to_string(index=False))


if __name__ == "__main__":
    main()
