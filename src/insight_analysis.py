# src/insight_analysis.py
# Purpose: Explore correlations and insights between key numeric features.
# Run: python src/insight_analysis.py

import os
import pandas as pd
import matplotlib.pyplot as plt

INPUT_PATH = os.path.join("data", "processed", "logistics_features.csv")
OUTPUT_PATH = os.path.join("data", "processed", "correlation_results.csv")

def main():
    if not os.path.exists(INPUT_PATH):
        raise FileNotFoundError(f"Expected file not found at {INPUT_PATH}")

    df = pd.read_csv(INPUT_PATH)

    # Select numeric columns for correlation analysis
    numeric_cols = df.select_dtypes(include=['number'])
    corr = numeric_cols.corr()

    # Save correlation results for Power BI import
    corr.to_csv(OUTPUT_PATH)
    print(f"Correlation results saved to: {OUTPUT_PATH}")

    # Simple visualization
    plt.figure(figsize=(8, 6))
    plt.imshow(corr, cmap='coolwarm', interpolation='nearest')
    plt.colorbar(label='Correlation')
    plt.xticks(range(len(corr.columns)), corr.columns, rotation=45, ha='right')
    plt.yticks(range(len(corr.columns)), corr.columns)
    plt.title('Feature Correlation Heatmap')
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()
