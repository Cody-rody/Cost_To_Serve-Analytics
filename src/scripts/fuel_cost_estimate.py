# src/fuel_cost_estimate.py
# Purpose: Calculate synthetic fuel cost estimates for logistics analysis.
# Run: python src/fuel_cost_estimate.py

import os
import pandas as pd

INPUT_PATH = os.path.join("data", "processed", "cleaned_logistics_data.csv")
OUTPUT_PATH = os.path.join("data", "processed", "logistics_features.csv")

TRAFFIC_MULT = {"Clear": 1.0, "Detour": 1.2, "Heavy": 1.5}

def safe_traffic_multiplier(val):
    return TRAFFIC_MULT.get(val, 1.0)

def main():
    if not os.path.exists(INPUT_PATH):
        raise FileNotFoundError(f"Expected file at: {INPUT_PATH}")

    df = pd.read_csv(INPUT_PATH, parse_dates=['Timestamp'])

    # Fill essential missing data
    df['Asset_Utilization'] = df['Asset_Utilization'].fillna(df['Asset_Utilization'].median())
    df['Waiting_Time'] = df['Waiting_Time'].fillna(df['Waiting_Time'].median())
    df['Traffic_Status'] = df['Traffic_Status'].fillna('Clear')

    # Fuel cost estimate
    base_cost = 100.0
    df['traffic_mult'] = df['Traffic_Status'].apply(safe_traffic_multiplier)
    df['utilization_factor'] = 1.0 + (1.0 - (df['Asset_Utilization'] / 100.0))
    df['waiting_factor'] = 1.0 + 0.1 * (df['Waiting_Time'] / 60.0)

    df['fuel_cost_estimate'] = (
        base_cost * df['utilization_factor'] * df['traffic_mult'] * df['waiting_factor']
    ).round(2)
    

    # Save output
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    df.to_csv(OUTPUT_PATH, index=False)

    print("Fuel cost feature added.")
    print("Saved to:", OUTPUT_PATH)
    print(df[['Asset_Utilization', 'Waiting_Time', 'Traffic_Status', 'fuel_cost_estimate']].head(6).to_string(index=False))

if __name__ == "__main__":
    main()
