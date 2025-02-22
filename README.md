Setting Up and Running Automated PUCC Log Analysis in GitHub Actions

Overview

This document provides step-by-step instructions on setting up an automated log analysis system using GitHub Actions. The workflow fetches the latest logs from GitHub, analyzes them, generates an HTML report, and publishes it using GitHub Pages for easy access.

1. Setting Up the GitHub Action Workflow

Step 1: Create the Workflow File

Navigate to your GitHub repository.

Create a new folder: .github/workflows/.

Inside this folder, create a new file: analyze_pucc_logs.yml.

Add the following content:

name: Analyze PUCC Logs

on:
  schedule:
    - cron: '0 0 * * *'  # Runs daily at 00:00 UTC (midnight)
  workflow_dispatch:

jobs:
  analyze:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout Repository
        uses: actions/checkout@v3

      - name: Set Up Python
        uses: actions/setup-python@v3
        with:
          python-version: '3.9'

      - name: Fetch Latest Logs from GitHub
        run: |
          git pull origin main
          ls logs/

      - name: Install Dependencies
        run: pip install pandas matplotlib

      - name: Run Log Analysis
        run: python analyze_pucc_logs.py

      - name: Upload Analysis Report
        uses: actions/upload-artifact@v4
        with:
          name: pucc-analysis-report
          path: pucc_analysis_report.html

      - name: Deploy HTML Report to GitHub Pages
        uses: peaceiris/actions-gh-pages@v3
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          publish_dir: .
          destination_dir: report

Step 2: Commit and Push the Workflow

Run the following commands in your terminal:

git add .github/workflows/analyze_pucc_logs.yml
git commit -m "Add GitHub Action for PUCC log analysis"
git push origin main

2. Python Script (analyze_pucc_logs.py)

Modify your script to automatically detect the most recent log file from the logs directory:

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

3. Running the Workflow

Manual Trigger

Go to GitHub → Your Repository.

Click on the "Actions" tab.

Find "Analyze PUCC Logs" workflow.

Click "Run workflow".

Automated Execution

The workflow will automatically run daily at midnight UTC based on the cron schedule.

4. Accessing the Report

Download the Report

After the workflow runs, go to "Actions".

Click on the latest workflow run.

Scroll to the "Artifacts" section.

Click "pucc-analysis-report" to download the report.

View the Report on GitHub Pages

Once deployed, you can access the report at:

https://wakanga.github.io/alfredpucc1/report/pucc_analysis_report.html

5. Final Steps

✅ Ensure logs are uploaded daily from the Raspberry Pi (already set up).✅ Check the Actions tab for errors if the report doesn’t generate.✅ Modify report visuals if needed for better clarity.

🚀 Your PUCC log analysis is now fully automated! Let me know if you need any improvements.
