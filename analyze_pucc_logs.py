import os
import pandas as pd
import matplotlib.pyplot as plt

# Identify the latest log file
logs_dir = "logs"
log_files = sorted([f for f in os.listdir(logs_dir) if f.endswith(".csv")])
latest_log = os.path.join(logs_dir, log_files[-1])  # Pick the most recent

# Load data
df = pd.read_csv(latest_log)

# Calculate uptime and downtime
uptime = df['status'].mean() * 100  # Percentage uptime
downtime = 100 - uptime  # Percentage downtime

# Generate visualizations
plt.pie([uptime, downtime], labels=['Uptime', 'Downtime'], autopct='%1.1f%%')
plt.title('PUCC Uptime vs. Downtime')
plt.savefig('uptime_downtime_pie.png')

# Generate HTML report
html_report = f"""
<!DOCTYPE html>
<html>
<head>
  <title>PUCC Log Analysis Report</title>
</head>
<body>
  <h1>PUCC Log Analysis Report</h1>
  <h2>Summary Statistics</h2>
  <p>Uptime: {uptime:.2f}%</p>
  <p>Downtime: {downtime:.2f}%</p>

  <h2>Visualizations</h2>
  <img src="uptime_downtime_pie.png" alt="Uptime/Downtime Pie Chart">
</body>
</html>
"""

with open("pucc_analysis_report.html", "w") as f:
    f.write(html_report)
