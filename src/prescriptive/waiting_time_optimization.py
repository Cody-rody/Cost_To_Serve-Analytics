# src/prescriptive/weather_optimization.py
"""
Prescriptive Module: Weather Optimization
-----------------------------------------
Analyzes the impact of temperature and humidity on logistics delay penalties,
and prescribes the most cost-efficient operational weather ranges.
"""

import pandas as pd
import numpy as np
import os

# -----------------------------
#  PATH CONFIGURATION
# -----------------------------
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
DATA_PATH = os.path.join(BASE_DIR, "data", "processed", "delay_penalty_cost.csv")
OUTPUT_PATH = os.path.join(BASE_DIR, "data", "processed", "weather_optimization_results.csv")

# -----------------------------
#  LOAD DATA
# -----------------------------
def load_data():
    """Load and normalize processed logistics data."""
    if not os.path.exists(DATA_PATH):
        raise FileNotFoundError(f"File not found: {DATA_PATH}")
    
    df = pd.read_csv(DATA_PATH)
    print(f"Data loaded successfully — {df.shape[0]} records, {df.shape[1]} columns.")
    
    # Normalize column names
    df.columns = df.columns.str.strip().str.lower()
    
    # Handle inconsistent naming
    if "delay_penalty_cost" in df.columns and "delay_penalty" not in df.columns:
        df.rename(columns={"delay_penalty_cost": "delay_penalty"}, inplace=True)
    if "temperature_c" in df.columns and "temperature" not in df.columns:
        df.rename(columns={"temperature_c": "temperature"}, inplace=True)
    if "humidity_percent" in df.columns and "humidity" not in df.columns:
        df.rename(columns={"humidity_percent": "humidity"}, inplace=True)

    return df

# -----------------------------
#  PREPROCESS
# -----------------------------
def preprocess(df):
    """Prepare data for weather-based analysis."""
    required_columns = ["temperature", "humidity", "delay_penalty"]
    for col in required_columns:
        if col not in df.columns:
            raise KeyError(f"Missing required column: {col}")

    df["temperature"] = pd.to_numeric(df["temperature"], errors="coerce").fillna(df["temperature"].median())
    df["humidity"] = pd.to_numeric(df["humidity"], errors="coerce").fillna(df["humidity"].median())
    df["delay_penalty"] = pd.to_numeric(df["delay_penalty"], errors="coerce").fillna(0)

    # Create temperature bins (in °C)
    temp_bins = [-np.inf, 10, 15, 20, 25, 30, 35, np.inf]
    temp_labels = ["<10°C", "10–15°C", "15–20°C", "20–25°C", "25–30°C", "30–35°C", ">35°C"]
    df["temp_range"] = pd.cut(df["temperature"], bins=temp_bins, labels=temp_labels)

    # Create humidity bins (in %)
    humidity_bins = [0, 20, 30, 40, 50, 60, 70, 80, np.inf]
    humidity_labels = ["0–20%", "20–30%", "30–40%", "40–50%", "50–60%", "60–70%", "70–80%", "80%+"]
    df["humidity_range"] = pd.cut(df["humidity"], bins=humidity_bins, labels=humidity_labels)

    return df

# -----------------------------
#  ANALYSIS
# -----------------------------
def analyze_weather_effect(df, min_records=10):
    """Find optimal temperature and humidity ranges with lowest delay penalty."""
    # Group by temperature and humidity range
    temp_summary = (
        df.groupby("temp_range")
        .agg(avg_penalty=("delay_penalty", "mean"), count=("delay_penalty", "count"))
        .reset_index()
    )
    humidity_summary = (
        df.groupby("humidity_range")
        .agg(avg_penalty=("delay_penalty", "mean"), count=("delay_penalty", "count"))
        .reset_index()
    )

    # Filter for significant sample size
    temp_summary = temp_summary[temp_summary["count"] >= min_records]
    humidity_summary = humidity_summary[humidity_summary["count"] >= min_records]

    if temp_summary.empty or humidity_summary.empty:
        print("Not enough data for meaningful weather recommendations.")
        return pd.DataFrame(), temp_summary, humidity_summary

    # Find optimal temperature and humidity bands
    optimal_temp = temp_summary.loc[temp_summary["avg_penalty"].idxmin()]
    optimal_humidity = humidity_summary.loc[humidity_summary["avg_penalty"].idxmin()]

    # Calculate cost improvement estimates
    current_avg_penalty = df["delay_penalty"].mean()
    min_avg_penalty = (optimal_temp["avg_penalty"] + optimal_humidity["avg_penalty"]) / 2
    estimated_savings = current_avg_penalty - min_avg_penalty

    # Prepare recommendations summary
    recommendations = pd.DataFrame({
        "Optimal_Temperature_Range": [optimal_temp["temp_range"]],
        "Optimal_Humidity_Range": [optimal_humidity["humidity_range"]],
        "Min_Avg_Penalty": [round(min_avg_penalty, 2)],
        "Current_Avg_Penalty": [round(current_avg_penalty, 2)],
        "Estimated_Savings_Per_Trip": [round(estimated_savings, 2)],
        "Temp_Records_Analyzed": [int(optimal_temp["count"])],
        "Humidity_Records_Analyzed": [int(optimal_humidity["count"])]
    })

    return recommendations, temp_summary, humidity_summary

# -----------------------------
#  SAVE RESULTS
# -----------------------------
def save_results(recommendations, temp_summary, humidity_summary):
    """Save prescriptive results to CSV."""
    recommendations.to_csv(OUTPUT_PATH, index=False)
    temp_summary.to_csv(OUTPUT_PATH.replace(".csv", "_temp_summary.csv"), index=False)
    humidity_summary.to_csv(OUTPUT_PATH.replace(".csv", "_humidity_summary.csv"), index=False)

    print(f"Results saved to:")
    print(f"  - {OUTPUT_PATH}")
    print(f"  - {OUTPUT_PATH.replace('.csv', '_temp_summary.csv')}")
    print(f"  - {OUTPUT_PATH.replace('.csv', '_humidity_summary.csv')}")

# -----------------------------
#  MAIN
# -----------------------------
def main():
    print("\nStarting Weather Optimization Analysis...\n")

    df = load_data()
    df = preprocess(df)
    recommendations, temp_summary, humidity_summary = analyze_weather_effect(df)

    if recommendations.empty:
        print("No valid weather recommendations generated.")
    else:
        save_results(recommendations, temp_summary, humidity_summary)
        print("\nRecommended Safe Operational Ranges:\n")
        print(recommendations.to_string(index=False))

if __name__ == "__main__":
    main()
