# src/data_visualization.py
# Purpose: Create scatter plots and bar charts to visualize logistics patterns.
# Run: python src/data_visualization.py
#
# What it shows:
# 1. Scatter plots → show relationships between numeric variables.
# 2. Bar charts → show average fuel cost by category (traffic status, vehicle type).

import os
import pandas as pd
import matplotlib.pyplot as plt

# Input file: uses the output of feature_engineering.py
INPUT_PATH = os.path.join("data", "processed", "logistics_features.csv")

def main():
    if not os.path.exists(INPUT_PATH):
        raise FileNotFoundError(f"Expected processed file at: {INPUT_PATH}")

    df = pd.read_csv(INPUT_PATH)

    # --- Scatter Plot 1: Asset Utilization vs Fuel Cost ---
    plt.figure(figsize=(7, 5))
    plt.scatter(df['Asset_Utilization'], df['fuel_cost_estimate'], color='royalblue', alpha=0.6)
    plt.title("Asset Utilization vs Fuel Cost", fontsize=14)
    plt.xlabel("Asset Utilization (%)")
    plt.ylabel("Fuel Cost Estimate (₹)")
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.tight_layout()
    os.makedirs("data/visuals", exist_ok=True)
    plt.savefig("data/visuals/scatter_utilization_vs_fuel.png")
    plt.show()

    # --- Scatter Plot 2: Waiting Time vs Fuel Cost ---
    plt.figure(figsize=(7, 5))
    plt.scatter(df['Waiting_Time'], df['fuel_cost_estimate'], color='darkorange', alpha=0.6)
    plt.title("Waiting Time vs Fuel Cost", fontsize=14)
    plt.xlabel("Waiting Time (minutes)")
    plt.ylabel("Fuel Cost Estimate (₹)")
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.tight_layout()
    plt.savefig("data/visuals/scatter_waiting_vs_fuel.png")
    plt.show()

    # --- Bar Chart 1: Average Fuel Cost by Traffic Status ---
    plt.figure(figsize=(6, 4))
    traffic_avg = df.groupby('Traffic_Status')['fuel_cost_estimate'].mean().sort_values()
    traffic_avg.plot(kind='bar', color=['green', 'gold', 'red'])
    plt.title("Average Fuel Cost by Traffic Status", fontsize=14)
    plt.ylabel("Average Fuel Cost (₹)")
    plt.xlabel("Traffic Status")
    plt.tight_layout()
    os.makedirs("data/visuals", exist_ok=True)
    plt.savefig("data/visuals/bar_traffic_vs_fuel.png")
    plt.show()

    # --- Bar Chart 2: Average Fuel Cost by Vehicle Type (if column exists) ---
    if 'Vehicle_Type' in df.columns:
        plt.figure(figsize=(6, 4))
        vehicle_avg = df.groupby('Vehicle_Type')['fuel_cost_estimate'].mean().sort_values()
        vehicle_avg.plot(kind='bar', color='skyblue')
        plt.title("Average Fuel Cost by Vehicle Type", fontsize=14)
        plt.ylabel("Average Fuel Cost (₹)")
        plt.xlabel("Vehicle Type")
        plt.tight_layout()
        plt.savefig("data/visuals/bar_vehicle_vs_fuel.png")
        plt.show()
    else:
        print("No 'Vehicle_Type' column found — skipping vehicle bar chart.")

    print("\nVisualizations complete. Check the 'data/visuals/' folder for saved images.")

if __name__ == "__main__":
    main()
