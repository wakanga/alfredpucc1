import os
import requests
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from io import StringIO

# GitHub Repository details
GITHUB_REPO = "https://raw.githubusercontent.com/wakanga/alfredpucc1/main/logs/"
LOG_PREFIX = "pucc_logs_"

# Fetch latest log file from GitHub
def fetch_latest_log():
    current_year_month = datetime.now().strftime('%Y_%m')
    log_url = f"{GITHUB_REPO}{LOG_PREFIX}{current_year_month}.csv"
    
    response = requests.get(log_url)
    if response.status_code == 200:
        log_data = StringIO(response.text)
        print(f"Fetched log file: {log_url}")
        return pd.read_csv(log_data)
    else:
        raise FileNotFoundError(f"Could not retrieve log file from {log_url}")

# Function to analyze logs
def analyze_logs(logs):
    current_time = datetime.now()
    logs['Timestamp'] = pd.to_datetime(logs['Timestamp'], errors='coerce')
    logs.dropna(subset=['Timestamp'], inplace=True)
    
    # Filter only manually triggered transitions from Available to Unavailable
    manual_transitions = logs[(logs['Previous Status'] == 'Available') & 
                              (logs['New Status'] == 'Unavailable') &
                              (~logs['Reason'].str.contains("Auto-switch", na=False))]
    
    last_7_days = manual_transitions[manual_transitions['Timestamp'] >= current_time - timedelta(days=7)]
    entire_period = logs['Timestamp'].max() - logs['Timestamp'].min() > timedelta(days=7)
    
    print("Analysis for the last 7 days:")
    print(f"Total manual transitions from Available to Unavailable: {len(last_7_days)}")
    print(last_7_days['Reason'].value_counts())
    plot_reason_counts(last_7_days, 'Last 7 Days')
    
    if entire_period:
        print("\nAnalysis for the entire log file:")
        print(f"Total manual transitions from Available to Unavailable: {len(manual_transitions)}")
        print(manual_transitions['Reason'].value_counts())
        plot_reason_counts(manual_transitions, 'Entire Log File')
        compare_last_7_days_to_entire_log(last_7_days, manual_transitions)

# Function to plot reason counts
def plot_reason_counts(df, title_suffix):
    if df.empty:
        print(f"No manual transitions recorded for {title_suffix}.")
        return
    
    reason_counts = df['Reason'].value_counts()
    plt.figure(figsize=(10, 6))
    reason_counts.plot(kind='bar', color='steelblue')
    plt.title(f'Manual Reasons for Status Change ({title_suffix})')
    plt.xlabel('Reason')
    plt.ylabel('Count')
    plt.xticks(rotation=45)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.savefig(f'status_change_analysis_{title_suffix.lower().replace(" ", "_")}.png')
    plt.show()

# Function to compare the last 7 days with the entire log file
def compare_last_7_days_to_entire_log(last_7_days, entire_log):
    if last_7_days.empty or entire_log.empty:
        print("Insufficient data for comparison.")
        return
    
    last_7_days_counts = last_7_days['Reason'].value_counts()
    entire_log_counts = entire_log['Reason'].value_counts()
    
    comparison_df = pd.DataFrame({'Last 7 Days': last_7_days_counts, 'Entire Log': entire_log_counts}).fillna(0)
    
    comparison_df.plot(kind='bar', figsize=(10, 6))
    plt.title('Comparison of Manual Reasons for Status Change')
    plt.xlabel('Reason')
    plt.ylabel('Count')
    plt.xticks(rotation=45)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.legend()
    plt.savefig('status_change_comparison.png')
    plt.show()

if __name__ == "__main__":
    logs = fetch_latest_log()
    analyze_logs(logs)
