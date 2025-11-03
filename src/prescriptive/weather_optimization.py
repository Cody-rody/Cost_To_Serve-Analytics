# src/prescriptive/weather_optimization.py
"""
Prescriptive Module: Weather Optimization
-----------------------------------------
Analyzes the effect of Temperature and Humidity on logistics performance.
Recommends optimal weather conditions to minimize operational cost and delay impact.
"""

import pandas as pd
import numpy as np
import os

# -----------------------------
#  PATH CONFIGURATION
# -----------------------------
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
DATA_PATH = os.path.join(BASE_DIR, "data", "processed", "asset_utilization_cost.csv")
OUTPUT_PATH = os.path.join(BASE_DIR, "data", "processed", "weather_optimization_results.csv")

# -----------------------------
#  LOAD DATA
# -----------------------------
def load_data():
    """Load and normalize logistics dataset."""
    if not os.path.exists(DATA_PATH):
        raise FileNotFoundError(f"File not found: {DATA_PATH}")

    df = pd.read_csv(DATA_PATH)
    print(f"Data loaded successfully — {df.shape[0]} records, {df.shape[1]} columns.")
    df.columns = df.columns.str.strip().str.lower()
    return df

# -----------------------------
#  PREPROCESS
# -----------------------------
def preprocess(df):
    """Ensure numeric fields and create weather bins."""
    for col in ["temperature", "humidity", "asset_utilization", "idle_cost", "cost_per_asset_utilization"]:
        if col not in df.columns:
            print(f"⚠️ Missing column '{col}', filling with zeros.")
            df[col] = 0
        df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)

    # Create bins for temperature and humidity
    temp_bins = [-np.inf, 20, 25, 30, 35, np.inf]
    temp_labels = ["<20°C", "20–25°C", "25–30°C", "30–35°C", ">35°C"]
    df["temp_range"] = pd.cut(df["temperature"], bins=temp_bins, labels=temp_labels)

    hum_bins = [-np.inf, 40, 60, 80, np.inf]
    hum_labels = ["<40%", "40–60%", "60–80%", ">80%"]
    df["humidity_range"] = pd.cut(df["humidity"], bins=hum_bins, labels=hum_labels)

    # Compute Weather Efficiency Index
    df["weather_efficiency"] = (
        (df["asset_utilization"] / (df["cost_per_asset_utilization"] + 1)) *
        (1 / (df["idle_cost"] + 1))
    ) * 100

    return df

# -----------------------------
#  ANALYSIS
# -----------------------------
def analyze_weather(df, min_trips_threshold=5):
    """Analyze average efficiency across weather conditions."""
    summary = (
        df.groupby(["temp_range", "humidity_range"])
        .agg(
            avg_efficiency=("weather_efficiency", "mean"),
            avg_cost=("cost_per_asset_utilization", "mean"),
            avg_utilization=("asset_utilization", "mean"),
            trips=("asset_id", "count")
        )
        .reset_index()
    )

    # Filter out bins with very few records
    summary = summary[summary["trips"] >= min_trips_threshold]

    if summary.empty:
        print("Not enough valid data for meaningful weather optimization.")
        return pd.DataFrame(), pd.DataFrame()

    # Identify optimal weather (highest efficiency)
    optimal_row = summary.loc[summary["avg_efficiency"].idxmax()]
    optimal_eff = optimal_row["avg_efficiency"]
    current_eff = df["weather_efficiency"].mean()
    potential_gain = round(optimal_eff - current_eff, 2)

    recommendations = pd.DataFrame({
        "Optimal_Temp_Range": [optimal_row["temp_range"]],
        "Optimal_Humidity_Range": [optimal_row["humidity_range"]],
        "Optimal_Avg_Efficiency": [round(optimal_eff, 2)],
        "Current_Avg_Efficiency": [round(current_eff, 2)],
        "Estimated_Improvement": [potential_gain],
        "Trips_Analyzed": [int(optimal_row["trips"])]
    })

    return recommendations, summary

# -----------------------------
#  SAVE RESULTS
# -----------------------------
def save_results(recommendations, summary):
    """Save results to CSV files."""
    recommendations.to_csv(OUTPUT_PATH, index=False)
    details_path = OUTPUT_PATH.replace(".csv", "_details.csv")
    summary.to_csv(details_path, index=False)
    print(f"Results saved to:\n  - {OUTPUT_PATH}\n  - {details_path}")

# -----------------------------
#  MAIN
# -----------------------------
def main():
    print("\nStarting Weather Optimization Analysis...\n")

    df = load_data()
    df = preprocess(df)
    recommendations, summary = analyze_weather(df)

    if recommendations.empty:
        print("No valid recommendations generated.")
    else:
        save_results(recommendations, summary)
        print("\nRecommended Weather Conditions for Optimal Operations:\n")
        print(recommendations.to_string(index=False))


if __name__ == "__main__":
    main()
