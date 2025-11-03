# src/pipeline_runner.py
# Purpose: Run the full logistics cost analysis pipeline with progress updates.
# Run: python src/pipeline_runner.py

import subprocess
import sys
import time
from termcolor import colored  # install via: pip install termcolor

# Define pipeline steps in order
STEPS = [
    ("Data Visualisation", "src/data_visualisation.py"),
    ("Fuel Cost Estimation", "src/scripts/fuel_cost_estimate.py"),
    ("Cost per Asset Utilization", "src/scripts/asset_utilization.py"),
    ("Handling Cost Estimation", "src/scripts/handling_cost_estimate.py"),
    ("Report Generation", "src/report_generator.py")
]


def run_step(name, script):
    print(colored(f"\n🚀 Starting: {name}", "cyan"))
    time.sleep(0.5)
    try:
        result = subprocess.run([sys.executable, script], check=True, capture_output=True, text=True)
        print(colored(f"{name} completed successfully.", "green"))
        if result.stdout:
            print(colored(result.stdout, "white"))
    except subprocess.CalledProcessError as e:
        print(colored(f"❌ Error during {name} stage!", "red"))
        print(colored(e.stderr or str(e), "yellow"))
        sys.exit(1)

def main():
    print(colored("\n=== LOGISTICS ANALYSIS PIPELINE START ===", "blue", attrs=["bold"]))
    start_time = time.time()

    for step_name, script_path in STEPS:
        run_step(step_name, script_path)

    total_time = time.time() - start_time
    print(colored(f"\n All stages completed in {total_time:.2f} seconds.", "green", attrs=["bold"]))
    print(colored("Final report available in: data/reports/summary_report.txt", "cyan"))

if __name__ == "__main__":
    main()
