
# src/prescriptive/driver_performance_optimization.py
"""
Prescriptive Module: Driver Performance Optimization
----------------------------------------------------
Analyzes driver-level performance using available asset utilization, waiting time,
and idle cost metrics. Provides efficiency insights and identifies improvement opportunities.
"""

import pandas as pd
import numpy as np
import os

# -----------------------------
#  PATH CONFIGURATION
# -----------------------------
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
DATA_PATH = os.path.join(BASE_DIR, "data", "processed", "asset_utilization_cost.csv")
OUTPUT_SUMMARY = os.path.join(BASE_DIR, "data", "processed", "driver_performance_summary.csv")
OUTPUT_INSIGHTS = os.path.join(BASE_DIR, "data", "processed", "driver_performance_insights.csv")

# -----------------------------
#  LOAD DATA
# -----------------------------
def load_data():
    """Load and normalize dataset."""
    if not os.path.exists(DATA_PATH):
        raise FileNotFoundError(f"File not found: {DATA_PATH}")
    
    df = pd.read_csv(DATA_PATH)
    print(f"Data loaded successfully — {df.shape[0]} records, {df.shape[1]} columns.")
    df.columns = df.columns.str.strip().str.lower()

    # Add synthetic driver IDs (simulate 10 drivers)
    if "driver_id" not in df.columns:
        df["driver_id"] = np.random.choice([f"D_{i}" for i in range(10)], size=len(df))

    return df

# -----------------------------
#  PREPROCESS
# -----------------------------
def preprocess(df):
    """Prepare and compute driver efficiency metrics."""
    required_cols = ["asset_utilization", "waiting_time", "idle_cost"]
    for col in required_cols:
        if col not in df.columns:
            print(f"⚠️ Missing column '{col}', filling with zeros.")
            df[col] = 0

    # Convert to numeric
    for col in required_cols:
        df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)

    # Compute efficiency using real available metrics
    df["efficiency"] = (
        (df["asset_utilization"] / (df["waiting_time"] + 1)) *
        (1 / (df["idle_cost"] + 1))
    ) * 100  # scale to percentage

    return df

# -----------------------------
#  ANALYSIS
# -----------------------------
def analyze_driver_performance(df):
    """Aggregate metrics per driver and classify performance tiers."""
    summary = (
        df.groupby("driver_id")
        .agg(
            avg_efficiency=("efficiency", "mean"),
            avg_asset_utilization=("asset_utilization", "mean"),
            avg_waiting_time=("waiting_time", "mean"),
            avg_idle_cost=("idle_cost", "mean"),
            trips=("driver_id", "count")
        )
        .reset_index()
    )

    # Define performance tiers dynamically
    mean_eff = summary["avg_efficiency"].mean()
    conditions = [
        summary["avg_efficiency"] >= mean_eff * 1.1,
        summary["avg_efficiency"] >= mean_eff * 0.9,
        summary["avg_efficiency"] < mean_eff * 0.9
    ]
    labels = ["High Performer", "Average", "Underperformer"]
    summary["Performance_Tier"] = np.select(conditions, labels, default="Unclassified")

    # Insights
    optimal_eff = round(mean_eff, 2)
    low_perf = summary.query("Performance_Tier == 'Underperformer'")
    est_improvement = 0 if low_perf.empty else round(optimal_eff - low_perf["avg_efficiency"].mean(), 2)

    insights = pd.DataFrame({
        "Optimal_Avg_Efficiency": [optimal_eff],
        "Estimated_Improvement_If_Low_Reaches_Optimal": [est_improvement],
        "Low_Performers_Count": [len(low_perf)],
        "Drivers_Analyzed": [summary.shape[0]]
    })

    return summary, insights

# -----------------------------
#  SAVE RESULTS
# -----------------------------
def save_results(summary, insights):
    summary.to_csv(OUTPUT_SUMMARY, index=False)
    insights.to_csv(OUTPUT_INSIGHTS, index=False)
    print("Results saved to data/processed/ folder (2 CSV files).")

# -----------------------------
#  MAIN
# -----------------------------
def main():
    print("\nStarting Driver Performance Optimization Analysis...\n")

    df = load_data()
    df = preprocess(df)
    summary, insights = analyze_driver_performance(df)

    save_results(summary, insights)

    print("\n Driver Performance Summary:\n")
    print(summary.to_string(index=False))
    print("\n Prescriptive Insights:\n")
    print(insights.to_string(index=False))


if __name__ == "__main__":
    main()
