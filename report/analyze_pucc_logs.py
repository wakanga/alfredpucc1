import os
import pandas as pd
import matplotlib.pyplot as plt

# Identify the latest log file
logs_dir = "logs"
log_files = sorted([f for f in os.listdir(logs_dir) if f.endswith(".csv")])
latest_log = os.path.join(logs_dir, log_files[-1])

# Load data
df = pd.read_csv(latest_log)

# Convert Timestamp to datetime
df['Timestamp'] = pd.to_datetime(df['Timestamp'], errors='coerce')

# Calculate manual transitions from Available to Unavailable
manual_transitions = df[(df['Previous Status'] == 'Available') &
                        (df['New Status'] == 'Unavailable') &
                        (~df['Reason'].str.contains("Auto-switch", na=False))]

total_manual_transitions = len(manual_transitions)
reason_counts = manual_transitions['Reason'].value_counts()

# Generate visualization
plt.figure(figsize=(10, 6))
reason_counts.plot(kind='bar', color='steelblue')
plt.title('Manual Reasons for PUCC Status Change')
plt.xlabel('Reason')
plt.ylabel('Count')
plt.xticks(rotation=45)
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.savefig('manual_reasons_bar.png')

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
  <p>Total manual transitions (Available → Unavailable): {total_manual_transitions}</p>
  
  <h2>Reasons Breakdown</h2>
  {reason_counts.to_frame().to_html()}
  
  <h2>Visualizations</h2>
  <img src="manual_reasons_bar.png" alt="Manual Reasons Bar Chart">
</body>
</html>
"""

with open("pucc_analysis_report.html", "w") as f:
    f.write(html_report)
