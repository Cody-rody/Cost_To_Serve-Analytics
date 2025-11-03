# src/scripts/asset_utilization_cost.py
# Purpose: Calculate Cost per Asset Utilization based on fuel cost, waiting time, and asset usage efficiency.

import pandas as pd
import os

def calculate_asset_utilization_cost(df, idle_cost_rate=2):
    """
    Calculates cost per asset utilization.
    Formula:
        Idle_Cost = Waiting_Time × idle_cost_rate
        Cost_per_Asset_Utilization = (fuel_cost_estimate + Idle_Cost) / Asset_Utilization
    """
    if 'fuel_cost_estimate' not in df.columns:
        raise ValueError("Missing column: 'fuel_cost_estimate'. Run fuel_cost_estimate.py first.")

    if 'Asset_Utilization' not in df.columns:
        # Generate approximate utilization based on Waiting_Time
        df['Asset_Utilization'] = (100 - df['Waiting_Time'] * 0.3).clip(lower=20) / 100
        print("Asset_Utilization column not found — generated approximate utilization based on Waiting_Time.")

    # Calculate Idle Cost
    df['Idle_Cost'] = df['Waiting_Time'] * idle_cost_rate

    # Calculate cost per asset utilization
    df['Cost_per_Asset_Utilization'] = (
        (df['fuel_cost_estimate'] + df['Idle_Cost']) / df['Asset_Utilization']
    ).round(2)

    return df


def main():
    input_path = "data/processed/logistics_features.csv"
    output_path = "data/processed/asset_utilization_cost.csv"
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    df = pd.read_csv(input_path)
    df = calculate_asset_utilization_cost(df)

    df.to_csv(output_path, index=False)
    print(f"Cost per Asset Utilization calculated and saved to: {output_path}")

    # Display quick summary
    print("\nSample of calculated values:")
    print(df[['fuel_cost_estimate', 'Waiting_Time', 'Asset_Utilization', 'Idle_Cost', 'Cost_per_Asset_Utilization']].head())


if __name__ == "__main__":
    main()
