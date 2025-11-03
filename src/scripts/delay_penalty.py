# src/scripts/delay_penalty.py
# Purpose: Calculate Delay Penalty (Service Deviation Cost) based on delays, waiting time, and traffic.
# Run: python src/scripts/delay_penalty.py

import os
import pandas as pd

def calculate_delay_penalty(df):
    """
    Formula:
        Delay_Penalty_Cost = base_penalty
                            + (Waiting_Time * time_penalty_rate)
                            * traffic_multiplier
                            + (extra_charge if Logistics_Delay == 1)

    Base penalty covers general operational disruption.
    Higher traffic = higher multiplier.
    """

    # --- Constants (in ₹) ---
    base_penalty = 50
    time_penalty_rate = 2.5
    delay_charge = 75

    # Traffic multipliers (same logic as earlier)
    TRAFFIC_MULT = {
        "Clear": 1.0,
        "Detour": 1.2,
        "Heavy": 1.5
    }

    # Fill missing data
    df['Traffic_Status'] = df['Traffic_Status'].fillna('Clear')
    df['Waiting_Time'] = df['Waiting_Time'].fillna(df['Waiting_Time'].median())
    df['Logistics_Delay'] = df['Logistics_Delay'].fillna(0)

    # Apply multiplier and formula
    df['traffic_mult'] = df['Traffic_Status'].map(lambda x: TRAFFIC_MULT.get(x, 1.0))
    df['Delay_Penalty_Cost'] = (
        base_penalty
        + (df['Waiting_Time'] * time_penalty_rate * df['traffic_mult'])
        + (df['Logistics_Delay'].apply(lambda x: delay_charge if x == 1 else 0))
    ).round(2)

    return df


def main():
    input_path = "data/processed/asset_utilization_cost.csv"
    output_path = "data/processed/delay_penalty_cost.csv"
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    df = pd.read_csv(input_path)
    df = calculate_delay_penalty(df)
    df.to_csv(output_path, index=False)

    print(f"Delay Penalty (Service Deviation Cost) calculated and saved to: {output_path}\n")
    print(df[['Waiting_Time', 'Traffic_Status', 'Logistics_Delay', 'Delay_Penalty_Cost']].head())


if __name__ == "__main__":
    main()
