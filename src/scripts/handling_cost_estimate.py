# src/handling_cost_estimate.py
# Purpose: Calculate synthetic handling cost estimates for logistics analysis.
# Run: python src/handling_cost_estimate.py

import os
import pandas as pd

INPUT_PATH = os.path.join("data", "processed", "logistics_features.csv")  # now read from output of previous metric
OUTPUT_PATH = os.path.join("data", "processed", "logistics_features.csv")

def main():
    if not os.path.exists(INPUT_PATH):
        raise FileNotFoundError(f"Expected file at: {INPUT_PATH}")

    df = pd.read_csv(INPUT_PATH, parse_dates=['Timestamp'])

    # Fill missing values
    df['Temperature'] = df['Temperature'].fillna(df['Temperature'].median())
    df['Humidity'] = df['Humidity'].fillna(df['Humidity'].median())
    df['Inventory_Level'] = df['Inventory_Level'].fillna(df['Inventory_Level'].median())
    df['Logistics_Delay'] = df['Logistics_Delay'].fillna(0)
    df['Traffic_Status'] = df['Traffic_Status'].fillna('Clear')

    # Parameters
    base_handling = 50.0
    waiting_min_rate = 0.20
    delay_penalty_amt = 30.0
    temp_penalty_amt = 20.0
    humidity_penalty_amt = 15.0
    complexity_fee_amt = 10.0

    TRAFFIC_MULT_HANDLE = {"Clear": 1.0, "Detour": 1.1, "Heavy": 1.2}

    def temp_penalty(temp): return temp_penalty_amt if (temp < 18 or temp > 27) else 0.0
    def humidity_penalty(h): return humidity_penalty_amt if (h > 75 or h < 40) else 0.0
    def complexity_fee(inv): return complexity_fee_amt if inv > 400 else 0.0

    df['traffic_mult_handle'] = df['Traffic_Status'].map(lambda x: TRAFFIC_MULT_HANDLE.get(x, 1.0))
    df['waiting_component'] = df['Waiting_Time'] * waiting_min_rate
    df['delay_penalty'] = df['Logistics_Delay'].apply(lambda x: delay_penalty_amt if x == 1 else 0.0)
    df['temp_penalty'] = df['Temperature'].apply(temp_penalty)
    df['humidity_penalty'] = df['Humidity'].apply(humidity_penalty)
    df['complexity_fee'] = df['Inventory_Level'].apply(complexity_fee)

    df['handling_cost_estimate'] = (
        (base_handling
         + df['waiting_component']
         + df['delay_penalty']
         + df['temp_penalty']
         + df['humidity_penalty']
         + df['complexity_fee'])
        * df['traffic_mult_handle']
    ).round(2)

    # Save output (overwriting with updated columns)
    df.to_csv(OUTPUT_PATH, index=False)

    print("Handling cost feature added.")
    print("Saved to:", OUTPUT_PATH)
    print(df[['Waiting_Time', 'Temperature', 'Humidity', 'Traffic_Status', 'handling_cost_estimate']].head(6).to_string(index=False))

if __name__ == "__main__":
    main()
