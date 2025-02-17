import os
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

# Path to the logs directory
logs_dir = 'logs'

def read_most_recent_log(logs_dir):
    log_files = [f for f in os.listdir(logs_dir) if f.endswith('.csv')]
    if not log_files:
        raise FileNotFoundError("No log files found in the logs directory.")
    # Assuming log files are named in a way that sorting them lexicographically gives the most recent file last
    most_recent_log = sorted(log_files)[-1]
    return pd.read_csv(os.path.join(logs_dir, most_recent_log))

def analyze_logs(logs):
    current_time = datetime.now()
    logs['Timestamp'] = pd.to_datetime(logs['Timestamp'])

    # Filter transitions from Available to Unavailable
    available_to_unavailable = logs[(logs['Previous Status'] == 'Available') & (logs['New Status'] == 'Unavailable')]
    
    # Analyze the last 7 days
    last_7_days = available_to_unavailable[available_to_unavailable['Timestamp'] >= current_time - timedelta(days=7)]
    
    # Analyze the entire log file if it spans more than 7 days
    if logs['Timestamp'].max() - logs['Timestamp'].min() > timedelta(days=7):
        entire_period = True
    else:
        entire_period = False
    
    # General statements
    print("Analysis for the last 7 days:")
    total_transitions_7_days = len(last_7_days)
    reasons_counts_7_days = last_7_days['Reason'].value_counts()
    print(f"Total transitions from Available to Unavailable: {total_transitions_7_days}")
    print("Reasons for transitions:")
    print(reasons_counts_7_days)

    # Plot the reasons for transitions in the last 7 days
    plt.figure(figsize=(10, 6))
    reasons_counts_7_days.plot(kind='bar')
    plt.title('Reasons for Status Change from Available to Unavailable (Last 7 Days)')
    plt.xlabel('Reason')
    plt.ylabel('Count')
    plt.xticks(rotation=45)
    plt.savefig('status_change_analysis_last_7_days.png')
    plt.show()

    if entire_period:
        print("\nAnalysis for the entire log file:")
        total_transitions = len(available_to_unavailable)
        reasons_counts = available_to_unavailable['Reason'].value_counts()
        print(f"Total transitions from Available to Unavailable: {total_transitions}")
        print("Reasons for transitions:")
        print(reasons_counts)

        # Plot the reasons for transitions in the entire log file
        plt.figure(figsize=(10, 6))
        reasons_counts.plot(kind='bar')
        plt.title('Reasons for Status Change from Available to Unavailable (Entire Log File)')
        plt.xlabel('Reason')
        plt.ylabel('Count')
        plt.xticks(rotation=45)
        plt.savefig('status_change_analysis_entire_log.png')
        plt.show()

if __name__ == '__main__':
    logs = read_most_recent_log(logs_dir)
    analyze_logs(logs)
