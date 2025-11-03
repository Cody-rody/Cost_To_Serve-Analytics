# src/enhanced_pipeline.py
# Purpose: Modular Logistics Cost & Optimization Pipeline with Logging, Error Handling, and Timestamped Outputs
# Run Example:
#   python src/enhanced_pipeline.py --stage all
#   python src/enhanced_pipeline.py --stage prescriptive
#   python src/enhanced_pipeline.py --stage analysis

import subprocess
import sys
import time
import argparse
import os
from datetime import datetime
from termcolor import colored

# ======= CONFIG =======
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DATA_DIR = os.path.join(BASE_DIR, "data")
LOG_DIR = os.path.join(DATA_DIR, "logs")

os.makedirs(LOG_DIR, exist_ok=True)

# Create timestamped folder for each pipeline run
timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
RUN_DIR = os.path.join(DATA_DIR, "processed", f"run_{timestamp}")
os.makedirs(RUN_DIR, exist_ok=True)

LOG_FILE = os.path.join(LOG_DIR, f"pipeline_log_{timestamp}.txt")

# ======= PIPELINE STAGES =======
STAGES = {
    "analysis": [
        ("Data Visualization", "src/data_visualisation.py"),
        ("Fuel Cost Estimation", "src/scripts/fuel_cost_estimate.py"),
        ("Asset Utilization Cost", "src/scripts/asset_utilization.py"),
        ("Handling Cost Estimation", "src/scripts/handling_cost_estimate.py"),
        ("Inventorry Holding Cost", "src/scripts/inventory_holding_cost.py"),
        ("Delay Penalty","src/scripts/delay_penalty.py"),
        ("Report Generation", "src/report_generator.py")
    ],
    "prescriptive": [
        ("Traffic Optimization", "src/prescriptive/traffic_optimization.py"),
        ("Waiting Time Optimization", "src/prescriptive/waiting_time_optimization.py"),
        ("Asset Utilization Optimization", "src/prescriptive/asset_utilization_optimization.py"),
        ("Weather Optimization", "src/prescriptive/weather_optimization.py"),
        ("Driver Performance Optimization", "src/prescriptive/driver_performance_optimization.py"),
    ]
}

# ======= HELPER FUNCTIONS =======
def log(message, color="white", write=True):
    """Print and optionally write to log file."""
    msg = f"[{datetime.now().strftime('%H:%M:%S')}] {message}"
    print(colored(msg, color))
    if write:
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(msg + "\n")


def run_step(name, script):
    """Run an individual pipeline step."""
    log(f" Starting: {name}", "cyan")
    start = time.time()
    try:
        result = subprocess.run([sys.executable, script], check=True, capture_output=True, text=True)
        duration = time.time() - start
        log(f" {name} completed in {duration:.2f} seconds.", "green")
        if result.stdout.strip():
            log(result.stdout.strip(), "white", write=False)
    except subprocess.CalledProcessError as e:
        log(f" Error in {name}: {e.stderr or e.stdout}", "red")
        return False
    return True


def run_pipeline(stage):
    """Run the selected pipeline stage(s)."""
    log("\n=== LOGISTICS PIPELINE EXECUTION STARTED ===", "blue")
    start_time = time.time()

    stages_to_run = []
    if stage == "all":
        stages_to_run = list(STAGES["analysis"]) + list(STAGES["prescriptive"])
    elif stage in STAGES:
        stages_to_run = STAGES[stage]
    else:
        log(f" Unknown stage '{stage}'. Use 'analysis', 'prescriptive', or 'all'.", "yellow")
        sys.exit(1)

    for step_name, script_path in stages_to_run:
        if not run_step(step_name, script_path):
            log(f" Pipeline halted at stage: {step_name}", "red")
            break

    total_time = time.time() - start_time
    log(f"\n Pipeline finished in {total_time:.2f} seconds.", "green", write=True)
    log(f" Logs saved at: {LOG_FILE}", "cyan", write=False)
    log(f" Outputs saved in: {RUN_DIR}", "cyan", write=False)


# ======= MAIN ENTRY =======
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run the Logistics Cost Analysis Pipeline")
    parser.add_argument("--stage", type=str, default="all",
                        help="Stage to run: 'analysis', 'prescriptive', or 'all'")
    args = parser.parse_args()

    run_pipeline(args.stage)
