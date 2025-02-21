import os
import pandas as pd
import matplotlib.pyplot as plt

# Identify the latest log file
logs_dir = "logs"
log_files = sorted([f for f in os.listdir(logs_dir) if f.endswith(".csv")])
latest_log = os.path.join(logs_dir, log_files[-1])

# Load data
df = pd.read_csv(latest_log)
df['Timestamp'] = pd.to_datetime(df['Timestamp'], errors='coerce')
df['Date'] = df['Timestamp'].dt.date

# Calculate total downtime per day
df['Duration'] = df['Timestamp'].diff().dt.total_seconds().div(60)  # Convert to minutes
daily_downtime = df[df['New Status'] == 'Unavailable'].groupby('Date')['Duration'].sum().fillna(0)

# Calculate daily uptime percentage
daily_status_counts = df.groupby(['Date', 'New Status']).size().unstack(fill_value=0)
daily_status_counts['Uptime %'] = (daily_status_counts['Available'] / (daily_status_counts['Available'] + daily_status_counts['Unavailable'])) * 100

# Generate visualizations
plt.figure(figsize=(10, 5))
daily_downtime.plot(kind='bar', color='darkred')
plt.xlabel("Date")
plt.ylabel("Total Minutes Offline")
plt.title("PUCC Daily Downtime (Minutes)")
plt.xticks(rotation=45)
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.savefig("daily_downtime.png")

plt.figure(figsize=(10, 5))
daily_status_counts['Uptime %'].plot(kind='line', marker='o', linestyle='-')
plt.xlabel("Date")
plt.ylabel("Uptime Percentage")
plt.title("Daily PUCC Uptime %")
plt.xticks(rotation=45)
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.savefig("daily_uptime_percentage.png")

# Generate HTML report
html_report = f"""
<!DOCTYPE html>
<html>
<head>
  <title>PUCC Log Analysis Report</title>
  <style>
    body {{ font-family: Arial, sans-serif; margin: 20px; }}
    h1, h2 {{ color: #333; }}
    table {{ border-collapse: collapse; width: 50%; margin-bottom: 20px; }}
    th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
    th {{ background-color: #f4f4f4; }}
    img {{ max-width: 100%; }}
  </style>
</head>
<body>
  <h1>PUCC Log Analysis Report</h1>
  <h2>Daily PUCC Downtime (Minutes)</h2>
  <img src="daily_downtime.png" alt="Daily Downtime">

  <h2>Daily PUCC Uptime Percentage</h2>
  <img src="daily_uptime_percentage.png" alt="Daily Uptime %">
</body>
</html>
"""

with open("pucc_analysis_report.html", "w") as f:
    f.write(html_report)
