# src/prescriptive/asset_utilization_optimization.py
"""
Prescriptive Module: Asset Utilization Optimization
---------------------------------------------------
Identifies utilization efficiency across assets (trucks), highlights underperformers,
and recommends an optimal utilization range to minimize cost per unit utilization.
"""

import pandas as pd
import numpy as np
import os

# -----------------------------
#  PATH CONFIGURATION
# -----------------------------
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
DATA_PATH = os.path.join(BASE_DIR, "data", "processed", "asset_utilization_cost.csv")
OUTPUT_PATH = os.path.join(BASE_DIR, "data", "processed", "asset_utilization_optimization_results.csv")

# -----------------------------
#  LOAD DATA
# -----------------------------
def load_data():
    """Load processed asset utilization dataset."""
    if not os.path.exists(DATA_PATH):
        raise FileNotFoundError(f"File not found: {DATA_PATH}")
    df = pd.read_csv(DATA_PATH)
    print(f" Data loaded successfully — {df.shape[0]} records, {df.shape[1]} columns.")
    return df

# -----------------------------
#  PREPROCESS
# -----------------------------
def preprocess(df):
    """Ensure correct column formats."""
    required_cols = ["Asset_ID", "Asset_Utilization", "Cost_per_Asset_Utilization", "Idle_Cost"]
    for col in required_cols:
        if col not in df.columns:
            raise KeyError(f"Missing column: {col}")

    for col in ["Asset_Utilization", "Cost_per_Asset_Utilization", "Idle_Cost"]:
        df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)
    
    return df

# -----------------------------
#  ANALYSIS
# -----------------------------
def analyze_utilization(df):
    """Analyze asset utilization and prescribe improvement actions."""

    # Group by asset to calculate mean utilization and costs
    asset_summary = (
        df.groupby("Asset_ID")
        .agg(
            avg_utilization=("Asset_Utilization", "mean"),
            avg_cost_per_util=("Cost_per_Asset_Utilization", "mean"),
            avg_idle_cost=("Idle_Cost", "mean"),
            trips=("Asset_ID", "count")
        )
        .reset_index()
    )

    # Calculate efficiency ratio (utilization / cost)
    asset_summary["efficiency_score"] = (
        asset_summary["avg_utilization"] / (asset_summary["avg_cost_per_util"] + 1e-5)
    ).round(2)

    # Determine performance tiers based on efficiency quantiles
    q_low = asset_summary["efficiency_score"].quantile(0.33)
    q_high = asset_summary["efficiency_score"].quantile(0.67)

    def performance_tier(row):
        if row["efficiency_score"] >= q_high:
            return "High Performer"
        elif row["efficiency_score"] <= q_low:
            return "Underperformer"
        else:
            return "Moderate Performer"

    asset_summary["Performance_Tier"] = asset_summary.apply(performance_tier, axis=1)

    # Find optimal utilization range
    bins = [0, 0.4, 0.6, 0.8, 1.0, np.inf]
    labels = ["0–40%", "40–60%", "60–80%", "80–100%", "100%+"]
    df["utilization_range"] = pd.cut(df["Asset_Utilization"], bins=bins, labels=labels, include_lowest=True)

    cost_summary = (
        df.groupby("utilization_range")
        .agg(
            avg_cost=("Cost_per_Asset_Utilization", "mean"),
            avg_utilization=("Asset_Utilization", "mean"),
            samples=("Asset_Utilization", "count")
        )
        .reset_index()
    )

    # Identify cost-optimal utilization range
    optimal_range = cost_summary.loc[cost_summary["avg_cost"].idxmin()]
    avg_cost_all = df["Cost_per_Asset_Utilization"].mean()
    potential_saving = avg_cost_all - optimal_range["avg_cost"]

    recommendations = pd.DataFrame({
        "Optimal_Utilization_Range": [optimal_range["utilization_range"]],
        "Min_Avg_Cost_per_Unit": [round(optimal_range["avg_cost"], 2)],
        "Current_Avg_Cost_per_Unit": [round(avg_cost_all, 2)],
        "Estimated_Savings_Per_Unit": [round(potential_saving, 2)],
        "Samples_Analyzed": [int(optimal_range["samples"])]
    })

    return asset_summary, cost_summary, recommendations

# -----------------------------
#  SAVE RESULTS
# -----------------------------
def save_results(asset_summary, cost_summary, recommendations):
    asset_summary.to_csv(OUTPUT_PATH.replace(".csv", "_asset_summary.csv"), index=False)
    cost_summary.to_csv(OUTPUT_PATH.replace(".csv", "_cost_summary.csv"), index=False)
    recommendations.to_csv(OUTPUT_PATH, index=False)
    print(f" Results saved to data/processed/ folder (3 CSV files).")

# -----------------------------
#  MAIN
# -----------------------------
def main():
    print("\nStarting Asset Utilization Optimization Analysis...\n")

    df = load_data()
    df = preprocess(df)
    asset_summary, cost_summary, recommendations = analyze_utilization(df)
    save_results(asset_summary, cost_summary, recommendations)

    print("\nRecommended Utilization Range to Minimize Cost:\n")
    print(recommendations.to_string(index=False))

    underperformers = asset_summary[asset_summary["Performance_Tier"] == "Underperformer"]
    print(f"\nUnderperforming Assets: {len(underperformers)} identified.")
    print(underperformers.head(10).to_string(index=False))


if __name__ == "__main__":
    main()
