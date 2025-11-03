# src/scripts/inventory_holding_cost.py
# Purpose: Calculate Inventory Holding Cost based on inventory levels and waiting time.

import pandas as pd
import os

def calculate_inventory_holding_cost(df, holding_cost_rate=0.05):
    """
    Formula:
        Inventory_Holding_Cost = Inventory_Level * holding_cost_rate * (1 + Waiting_Time / 60)
    """
    if 'Inventory_Level' not in df.columns or 'Waiting_Time' not in df.columns:
        raise ValueError("Missing required columns: 'Inventory_Level' or 'Waiting_Time'.")

    df['Inventory_Holding_Cost'] = (
        df['Inventory_Level'] * holding_cost_rate * (1 + df['Waiting_Time'] / 60)
    ).round(2)

    return df


def main():
    input_path = "data/processed/asset_utilization_cost.csv"
    output_path = "data/processed/inventory_holding_cost.csv"
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    df = pd.read_csv(input_path)
    df = calculate_inventory_holding_cost(df)

    df.to_csv(output_path, index=False)
    print(f"Inventory Holding Cost calculated and saved to: {output_path}\n")
    print(df[['Inventory_Level', 'Waiting_Time', 'Inventory_Holding_Cost']].head())


if __name__ == "__main__":
    main()
