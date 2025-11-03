# src/data_analysis.py
import pandas as pd

# Load the cleaned dataset
data = pd.read_csv("data/processed/cleaned_logistics_data.csv")

print("=== DATA ANALYSIS STARTED ===")

# 1. Check if longer waiting times mean more delays
avg_waiting_delay = data.groupby("Logistics_Delay")["Waiting_Time"].mean()
print("\nAverage waiting time comparison:")
print(avg_waiting_delay)

# 2. Check how traffic affects delays
traffic_delay = pd.crosstab(data["Traffic_Status"], data["Logistics_Delay"], normalize='index') * 100
print("\nDelay percentages under different traffic conditions:")
print(traffic_delay)

# 3. Check which delay reasons are most common
delay_reason_counts = data["Logistics_Delay_Reason"].value_counts()
print("\nMost common delay reasons:")
print(delay_reason_counts)

print("\n=== ANALYSIS COMPLETE ===")
