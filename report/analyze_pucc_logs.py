import os
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib

# Use a non-interactive backend for Matplotlib
matplotlib.use('Agg')

# Identify the latest log file
logs_dir = "logs"
log_files = sorted([f for f in os.listdir(logs_dir) if f.endswith(".csv")])
latest_log = os.path.join(logs_dir, log_files[-1])

# Load data
df = pd.read_csv(latest_log)
df['Timestamp'] = pd.to_datetime(df['Timestamp'], errors='coerce')
df['Date'] = df['Timestamp'].dt.date
df['Hour'] = df['Timestamp'].dt.hour

# Filter out expected downtime between 21:00 and 08:00
df = df[~((df['Hour'] >= 21) | (df['Hour'] < 8))]

# Calculate total downtime per day
df['Duration'] = df['Timestamp'].diff().dt.total_seconds().div(60)  # Convert to minutes
daily_downtime = df[df['New Status'] == 'Unavailable'].groupby('Date')['Duration'].sum().fillna(0)

# Calculate daily uptime percentage
daily_status_counts = df.groupby(['Date', 'New Status']).size().unstack(fill_value=0)
daily_status_counts['Uptime %'] = (daily_status_counts['Available'] / 
                                    (daily_status_counts['Available'] + daily_status_counts['Unavailable'])) * 100

# Generate visualizations
plt.figure(figsize=(10, 5))
daily_downtime.plot(kind='bar', color='darkred')
plt.xlabel("Date")
plt.ylabel("Total Minutes Offline")
plt.title("PUCC Daily Downtime (Minutes)")
plt.xticks(rotation=45)
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.subplots_adjust(bottom=0.2)
plt.savefig("daily_downtime.png")
plt.close()

plt.figure(figsize=(10, 5))
daily_status_counts['Uptime %'].plot(kind='line', marker='o', linestyle='-')
plt.xlabel("Date")
plt.ylabel("Uptime Percentage")
plt.title("Daily PUCC Uptime %")
plt.xticks(rotation=45)
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.subplots_adjust(bottom=0.2)
plt.savefig("daily_uptime_percentage.png")
plt.close()

# Generate pie chart for availability reasons
filtered_reasons = df[df['Reason'].isin(['full', 'no staff', 'not specified'])]
reason_counts = filtered_reasons['Reason'].value_counts()

if not reason_counts.empty:
    plt.figure(figsize=(8, 8))
    reason_counts.plot(kind='pie', autopct='%1.1f%%', startangle=90)
    plt.title("Proportion of Unavailability Reasons")
    plt.ylabel("")
    plt.savefig("availability_reasons.png")
    plt.close()
else:
    print("No valid unavailability reasons found, skipping pie chart.")

# Create availability changes table
availability_changes = df[(df['New Status'] == 'Unavailable') & 
                          (~df['Reason'].isin(['Auto-switch at configured time', 'auto reset after countdown']))].copy()
availability_changes['Change Time'] = availability_changes['Timestamp'].dt.strftime('%Y-%m-%d %H:%M:%S')
availability_table_html = availability_changes[['Timestamp', 'Date', 'Change Time', 'New Status', 'Reason']].to_html(index=False)

# Convert data to HTML tables
daily_downtime_html = daily_downtime.to_frame().rename(columns={"Duration": "Total Minutes Offline"}).to_html()
daily_uptime_html = daily_status_counts[['Uptime %']].to_html()

# Summary data
total_downtime = daily_downtime.sum()
average_uptime = daily_status_counts['Uptime %'].mean()
most_common_reason = reason_counts.idxmax() if not reason_counts.empty else 'N/A'

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
  <h2>Summary</h2>
  <p>Total Downtime: {total_downtime:.2f} minutes</p>
  <p>Average Uptime Percentage: {average_uptime:.2f}%</p>
  <p>Most Common Reason for Unavailability: {most_common_reason}</p>

  <h2>Daily PUCC Downtime (Minutes)</h2>
  {daily_downtime_html}
  <img src="daily_downtime.png" alt="Daily Downtime">

  <h2>Daily PUCC Uptime Percentage</h2>
  {daily_uptime_html}
  <img src="daily_uptime_percentage.png" alt="Daily Uptime %">

  <h2>Proportion of Unavailability Reasons</h2>
  <img src="availability_reasons.png" alt="Availability Reasons">

  <h2>Availability Changes</h2>
  {availability_table_html}
</body>
</html>
"""

with open("pucc_analysis_report.html", "w") as f:
    f.write(html_report)

print("Report generated successfully!")
