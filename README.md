# 🚢 Cost-to-Serve Analytics — Prescriptive Logistics Optimization
![Python](https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=white) ![Pandas](https://img.shields.io/badge/Pandas-150458?logo=pandas&logoColor=white) ![NumPy](https://img.shields.io/badge/NumPy-013243?logo=numpy&logoColor=white) ![PowerBI](https://img.shields.io/badge/PowerBI-F2C811?logo=power-bi&logoColor=black)

## 📌 Overview
This project implements a **single-source, end-to-end prescriptive analytics system** for logistics cost optimization using **Python, Pandas, NumPy, and Power BI**.  
It automates metric computation (fuel, handling, inventory, delay, utilization), runs **prescriptive modules** (traffic, waiting time, asset utilization, weather, driver performance), and provides **Power BI dashboards** for business decision-making.

---

## ⚙️ Project Structure
```bash
logistics_cost_analysis/
│
├── data/                             # All project data and outputs
│   ├── raw/                          # Original dataset(s)
│   ├── processed/                    # Cleaned & generated CSVs (module outputs)
│   ├── reports/                      # Auto-generated summaries (text)
│   └── logs/                         # Pipeline logs with timestamps
│
├── src/                              # All scripts and modules
│   ├── scripts/                      # Core cost computation modules
│   │   ├── fuel_cost_estimate.py
│   │   ├── handling_cost_estimate.py
│   │   ├── inventory_holding_cost.py
│   │   ├── delay_penalty.py
│   │   └── asset_utilization.py
│   │
│   ├── prescriptive/                 # Optimization & recommendation modules
│   │   ├── traffic_optimization.py
│   │   ├── waiting_time_optimization.py
│   │   ├── asset_utilization_optimization.py
│   │   ├── weather_optimization.py
│   │   └── driver_performance_optimization.py
│   │
│   ├── data_visualisation.py         # Power BI-ready visual generation
│   ├── report_generator.py           # Text report creation
│   ├── enhanced_pipeline.py          # Modular pipeline with logging & stages
│   └── run_pipeline.py               # Legacy/simple pipeline runner
│
├── prescriptive_visuals.pbix         # Power BI dashboards (prescriptive visuals)
├── requirements.txt                  # Python dependencies
└── README.md                         # Documentation
````

---

## 🚀 Workflow

1️⃣ **Data Preparation** — Load, clean, normalize raw logistics data.
2️⃣ **Feature Engineering** — Compute metrics like fuel cost, handling cost, inventory cost, delay penalty, and asset utilization cost.
3️⃣ **Prescriptive Modeling** — Optimization modules identify cost-efficient operating conditions.
4️⃣ **Pipeline Execution** — `enhanced_pipeline.py` runs the full or stage-wise pipeline with timestamped logs and outputs.
5️⃣ **Visualization Layer** — Power BI dashboards communicate actionable insights.

---

## 🧠 Prescriptive Modules

### 1️⃣ Traffic Optimization

Analyzes weekday-hour patterns of delay penalties and prescribes **best dispatch hours**.
**Output:** `traffic_optimization_results.csv`

### 2️⃣ Waiting Time Optimization

Finds **optimal waiting thresholds** for reduced idle costs.
**Output:** `waiting_time_optimization_results.csv`

### 3️⃣ Asset Utilization Optimization

Identifies **underperforming assets** and **optimal utilization ranges**.
**Output:** `asset_utilization_optimization_results.csv`

### 4️⃣ Weather Optimization

Correlates temperature and humidity with penalties to find **safe operational ranges**.
**Output:** `weather_optimization_results.csv`

### 5️⃣ Driver Performance Optimization

Measures efficiency, idle cost, and waiting patterns to tier drivers as **High**, **Average**, or **Underperformer**.
**Output:** `driver_performance_optimization_results.csv`

---

## 📊 Power BI Dashboard Layout

| Page | Focus              | Description                                  |
| ---- | ------------------ | -------------------------------------------- |
| 1    | Summary Dashboard  | KPIs — Savings, Recommendations, Avg Penalty |
| 2    | Waiting Time       | Penalty by waiting bin and total trips       |
| 3    | Traffic            | Dispatch hours by day and penalty trend      |
| 4    | Asset Utilization  | Cost per utilization vs efficiency           |
| 5    | Weather Impact     | Temp/Humidity correlation with cost          |
| 6    | Driver Performance | Efficiency vs utilization by tier            |

---

## 💼 Business Impact

* ⏱️ Reduced analysis time by **80%** through automation
* 💰 Identified **key cost-saving levers** in operations
* 🧩 Created modular framework for **easy extension**
* 📈 Translated analytics into **visual executive insights**

---

## 📁 Example Outputs

### 🔹 Traffic Optimization

```
DayOfWeek  Recommended_Hour  Traffic_Status  Min_Avg_Penalty  Trips_Analyzed
Friday     18                Detour          0.00              5
Monday     10                Clear           7.50              8
```

### 🔹 Waiting Time Optimization

```
Optimal_Waiting_Range  Min_Avg_Penalty  Current_Avg_Penalty  Estimated_Savings_Per_Trip
40–50                  15.64            16.98                 1.34
```

### 🔹 Asset Utilization Optimization

```
Optimal_Utilization_Range  Min_Avg_Cost_per_Unit  Current_Avg_Cost_per_Unit  Estimated_Savings_Per_Unit
100%+                      2.94                   2.94                         0.00
```

### 🔹 Weather Optimization

```
Optimal_Temperature_Range  Optimal_Humidity_Range  Estimated_Savings_Per_Trip
25–30°C                    50–60%                  2.14
```

### 🔹 Driver Performance Optimization

```
driver_id  avg_efficiency  avg_asset_utilization  avg_waiting_time  avg_idle_cost  trips  Performance_Tier
D_9        7.81            78.73                  32.55             65.10          107    High Performer
D_8        4.83            78.97                  38.53             77.06           98    Underperformer
```

---

## 🛠️ Tech Stack

* **Python 3.12+** — core computation
* **Pandas, NumPy** — data wrangling & numerical analysis
* **Power BI** — business visualization
* **Git & GitHub** — version control

---

## ⚙️ Installation & Setup

```bash
# 1️⃣ Clone the repository
git clone https://github.com/Cody-rody/Cost_To_Serve-Analytics.git
cd Cost_To_Serve-Analytics

# 2️⃣ Create & activate virtual environment
python -m venv venv
venv\Scripts\activate       # Windows
# source venv/bin/activate  # Mac/Linux

# 3️⃣ Install dependencies
pip install -r requirements.txt

# 4️⃣ Run the entire pipeline
python src/enhanced_pipeline.py --stage all

# Optional: run only prescriptive analytics
python src/enhanced_pipeline.py --stage prescriptive
```

---

## 🎯 Key Learnings

* Designed a **complete prescriptive analytics pipeline** from scratch
* Implemented **robust error handling and modular scripts**
* Automated data transformation and optimization flow
* Translated complex analytics into **Power BI dashboards**
* Learned **cost-to-serve analysis** for real-world logistics

---

## 🚀 Future Enhancements

* Integrate with **PostgreSQL** for relational data storage
* Use **Apache Airflow** for automated scheduling
* Enable **real-time Power BI dashboards**
* Expand to **predictive modeling** with ML for demand forecasting

---

## 👨‍💻 Author

**Sanketh Dappur**
🎓 *B.Tech in ECE | Aspiring Data Engineer*
🔗 [GitHub](https://github.com/Cody-rody)

---

## 🧾 License

**MIT License** — open for educational and professional use.

