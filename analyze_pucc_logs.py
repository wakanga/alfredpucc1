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

# Generate visualizations with increased margin
plt.figure(figsize=(10, 5))
daily_downtime.plot(kind='bar', color='darkred')
plt.xlabel("Date")
plt.ylabel("Total Minutes Offline")
plt.title("PUCC Daily Downtime (Minutes)")
plt.xticks(rotation=45)
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.subplots_adjust(bottom=0.2)  # Increase bottom margin
plt.savefig("daily_downtime.png")

plt.figure(figsize=(10, 5))
daily_status_counts['Uptime %'].plot(kind='line', marker='o', linestyle='-')
plt.xlabel("Date")
plt.ylabel("Uptime Percentage")
plt.title("Daily PUCC Uptime %")
plt.xticks(rotation=45)
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.subplots_adjust(bottom=0.2)  # Increase bottom margin
plt.savefig("daily_uptime_percentage.png")

# Create table of available-to-unavailable changes and times
availability_changes = df[df['New Status'] == 'Unavailable'].copy()
availability_changes['Change Time'] = availability_changes['Timestamp'].dt.strftime('%Y-%m-%d %H:%M:%S')
availability_table_html = availability_changes[['Timestamp', 'Date', 'Change Time', 'New Status']].to_html(index=False)

# Convert downtime and uptime data to HTML tables
daily_downtime_html = daily_downtime.to_frame().rename(columns={"Duration": "Total Minutes Offline"}).to_html()
daily_uptime_html = daily_status_counts[['Uptime %']].to_html()

# Generate HTML report
html_report = f"""
<!DOCTYPE html>
<html>
<head>
  <title>PUCC Log Analysis Report</title>
  <style>
    body {{ font-family: Arial, sans-serif; margin: 20px; }}
    h1, h2 {{ color: #333; }}
    table {{ border-collapse: collapse; width: 60%; margin-bottom: 20px; }}
    th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
    th {{ background-color: #f4f4f4; }}
    p {{ font-size: 14px; color: #555; }}
    img {{ max-width: 100%; }}
  </style>
</head>
<body>
  <h1>PUCC Log Analysis Report</h1>
  <h2>Daily PUCC Downtime (Minutes)</h2>
  <p>The table below shows how long PUCC was unavailable each day.</p>
  {daily_downtime_html}
  <img src="daily_downtime.png" alt="Daily Downtime">

  <h2>Daily PUCC Uptime Percentage</h2>
  <p>This table shows the percentage of time PUCC was available each day.</p>
  {daily_uptime_html}
  <img src="daily_uptime_percentage.png" alt="Daily Uptime %">

  <h2>Availability Changes</h2>
  <p>This table shows all available-to-unavailable changes and their times.</p>
  {availability_table_html}
</body>
</html>
"""

with open("pucc_analysis_report.html", "w") as f:
    f.write(html_report)
