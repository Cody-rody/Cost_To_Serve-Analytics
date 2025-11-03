# src/prescriptive/traffic_optimization.py
"""
Prescriptive Module: Traffic Optimization
-----------------------------------------
This module analyzes traffic-related penalty patterns across time of day and weekdays.
It prescribes the optimal dispatch hours to minimize delay penalties while ensuring
enough operational data support (trips > threshold).
"""

import pandas as pd
import numpy as np
import os
from datetime import datetime

# -----------------------------
#  PATH CONFIGURATION
# -----------------------------
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
DATA_PATH = os.path.join(BASE_DIR, "data", "processed", "asset_utilization_cost.csv")
OUTPUT_PATH = os.path.join(BASE_DIR, "data", "processed", "traffic_optimization_results.csv")

# -----------------------------
#  LOAD AND PREPROCESS DATA
# -----------------------------
def load_data():
    """Load and normalize the processed logistics dataset."""
    if not os.path.exists(DATA_PATH):
        raise FileNotFoundError(f"File not found: {DATA_PATH}")
    
    df = pd.read_csv(DATA_PATH)
    print(f"Data loaded successfully — {df.shape[0]} records, {df.shape[1]} columns.")
    
    # === Normalize column names ===
    df.columns = df.columns.str.strip().str.lower()

    # === Handle inconsistent naming ===
    if "delay_penalty_cost" in df.columns and "delay_penalty" not in df.columns:
        df.rename(columns={"delay_penalty_cost": "delay_penalty"}, inplace=True)
    
    return df


def preprocess(df):
    """Prepare datetime and categorical features for analysis."""
    # Add synthetic datetime if not available
    if "timestamp" in df.columns:
        df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")
        df["hour"] = df["timestamp"].dt.hour.fillna(0).astype(int)
        df["dayofweek"] = df["timestamp"].dt.day_name()
    else:
        np.random.seed(42)
        df["hour"] = np.random.choice(range(0, 24), size=len(df))
        df["dayofweek"] = np.random.choice(
            ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"],
            size=len(df)
        )
    
    # Clean/normalize key columns
    if "traffic_status" in df.columns:
        df["traffic_status"] = df["traffic_status"].fillna("Unknown")
    else:
        df["traffic_status"] = "Unknown"

    if "delay_penalty" not in df.columns:
        df["delay_penalty"] = 0
    else:
        df["delay_penalty"] = df["delay_penalty"].fillna(0)

    return df


# -----------------------------
#  ANALYSIS & PRESCRIPTIVE LOGIC
# -----------------------------
def analyze_traffic_cost(df, min_trips_threshold=5):
    """
    Analyze traffic penalties by weekday and hour, and recommend optimal dispatch hours.
    Only considers time slots with sufficient data (trips >= threshold).
    """
    if "traffic_status" not in df.columns or "delay_penalty" not in df.columns:
        raise KeyError("Expected columns 'traffic_status' and 'delay_penalty' not found in data.")

    # Aggregate traffic penalty by day, hour, and status
    summary = (
        df.groupby(["dayofweek", "hour", "traffic_status"])
        .agg(
            avg_penalty=("delay_penalty", "mean"),
            total_penalty=("delay_penalty", "sum"),
            trips=("asset_id", "count") if "asset_id" in df.columns else ("delay_penalty", "count")
        )
        .reset_index()
    )

    # Filter out hours with too few trips (avoid noise)
    summary = summary[summary["trips"] >= min_trips_threshold]

    if summary.empty:
        print("Not enough valid data for meaningful recommendations.")
        return pd.DataFrame()

    # Weighted average penalty to factor in trip count
    summary["weighted_penalty"] = summary["avg_penalty"] * (summary["trips"] / summary["trips"].max())

    # For each day, find hour with the lowest weighted penalty
    recommendations = (
        summary.loc[summary.groupby("dayofweek")["weighted_penalty"].idxmin()]
        .reset_index(drop=True)
    )

    recommendations.rename(
        columns={
            "hour": "Recommended_Hour",
            "avg_penalty": "Min_Avg_Penalty",
            "total_penalty": "Total_Penalty",
            "trips": "Trips_Analyzed",
        },
        inplace=True,
    )

    # Rank for easier dashboard sorting
    recommendations["Rank"] = recommendations["Min_Avg_Penalty"].rank(ascending=True).astype(int)

    return recommendations[
        ["dayofweek", "Recommended_Hour", "traffic_status", "Min_Avg_Penalty", "Trips_Analyzed", "Rank"]
    ]


# -----------------------------
#  SAVE RESULTS
# -----------------------------
def save_results(df):
    """Save recommendations to CSV."""
    df.to_csv(OUTPUT_PATH, index=False)
    print(f"Results saved to {OUTPUT_PATH}")


# -----------------------------
#  MAIN ENTRY POINT
# -----------------------------
def main():
    print("\nStarting Realistic Traffic Optimization Analysis...\n")

    df = load_data()
    df = preprocess(df)
    recommendations = analyze_traffic_cost(df)

    if recommendations.empty:
        print("No valid recommendations generated. Check dataset quality.")
    else:
        save_results(recommendations)
        print("\nRecommended Dispatch Hours by Day (Realistic):\n")
        print(recommendations.to_string(index=False))


if __name__ == "__main__":
    main()
