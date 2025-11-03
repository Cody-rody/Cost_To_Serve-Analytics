# src/report_generator.py
# Purpose: Automatically create a text-based summary report of our logistics analysis.
# Run: python src/report_generator.py

import os
import pandas as pd

INPUT_PATH = os.path.join("data", "processed", "logistics_features.csv")
REPORT_PATH = os.path.join("data", "reports", "summary_report.txt")

def main():
    if not os.path.exists(INPUT_PATH):
        raise FileNotFoundError(f"Expected features file at: {INPUT_PATH}")

    df = pd.read_csv(INPUT_PATH)
    os.makedirs(os.path.dirname(REPORT_PATH), exist_ok=True)

    # Prepare a few summary statistics
    avg_waiting_time = df['Waiting_Time'].mean()
    avg_fuel_cost = df['fuel_cost_estimate'].mean()
    avg_utilization = df['Asset_Utilization'].mean()

    # Write these into the report file
    with open(REPORT_PATH, "w", encoding="utf-8") as f:
        f.write("=== LOGISTICS PERFORMANCE REPORT ===\n\n")
        f.write(f"Average Waiting Time: {avg_waiting_time:.2f} minutes\n")
        f.write(f"Average Fuel Cost Estimate: ₹{avg_fuel_cost:.2f}\n")
        f.write(f"Average Asset Utilization: {avg_utilization:.2f}%\n")
        f.write("\n=== INSIGHTS & RECOMMENDATIONS ===\n")

        # Insight 1: Fuel cost efficiency
        if avg_fuel_cost > 160:
            f.write("- Fuel costs are relatively high. Consider optimizing routes or reducing idle time.\n")
        else:
            f.write("- Fuel costs appear under control compared to utilization.\n")

        # Insight 2: Waiting time analysis
        if avg_waiting_time > 40:
            f.write("- High waiting time indicates potential scheduling inefficiencies.\n")
        elif avg_waiting_time < 25:
            f.write("- Waiting time is well managed.\n")
        else:
            f.write("- Waiting times are moderate. Continuous monitoring recommended.\n")

        # Insight 3: Utilization commentary
        if avg_utilization < 70:
            f.write("- Asset utilization is low; consider better load distribution.\n")
        elif avg_utilization > 85:
            f.write("- Assets are highly utilized — monitor for overuse or maintenance needs.\n")
        else:
            f.write("- Asset utilization is at a healthy balance.\n")

    print("Report generated successfully at:", REPORT_PATH)

if __name__ == "__main__":
    main()
