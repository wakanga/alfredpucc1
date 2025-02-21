import tkinter as tk
from tkinter import messagebox
import csv
import os
import yaml
from datetime import datetime, timedelta
from threading import Timer
from PIL import Image, ImageTk
import subprocess

# ------------------ CONFIGURATION ------------------
CONFIG_PATH = "/home/alfredpi1/pucc_config.yaml"

# Load configuration
def load_config():
    """Load configuration from YAML file, or use default values if missing."""
    default_config = {
        "logo_path": "/home/alfredpi1/Alfred_Emergency_Logo.jpg",
        "log_dir": "/home/alfredpi1/logs",
        "status_file": "/home/alfredpi1/pucc_status.txt",
        "available_color": "#28a745",
        "unavailable_color": "#dc3545",
        "button_color": "#007BFF",
        "auto_unavailable_time": "21:00",
        "screen_off_time": "22:00",
        "screen_on_time": "06:00",
        "fullscreen": True
    }

    try:
        with open(CONFIG_PATH, "r") as f:
            return yaml.safe_load(f)
    except (FileNotFoundError, yaml.YAMLError):
        return default_config

config = load_config()

# Ensure log directory exists
if not os.path.exists(config["log_dir"]):
    os.makedirs(config["log_dir"])

# ------------------ STATUS MANAGEMENT ------------------
status = "Available"
status_end_time = None

# Load last known status if available
if os.path.exists(config["status_file"]):
    with open(config["status_file"], "r") as f:
        status = f.read().strip()

# Log status change
def log_status_change(prev_status, new_status, reason=""):
    """Logs status changes along with the reason."""
    now = datetime.now()
    log_filename = f"{config['log_dir']}/pucc_logs_{now.strftime('%Y_%m')}.csv"

    try:
        with open(log_filename, mode='a', newline='') as log_file:
            writer = csv.writer(log_file)
            if os.stat(log_filename).st_size == 0:
                writer.writerow(["Timestamp", "Previous Status", "New Status", "Reason"])
            writer.writerow([now.strftime("%Y-%m-%d %H:%M:%S"), prev_status, new_status, reason])
    except Exception as e:
        subprocess.run(["logger", f"Error logging to CSV: {e}"])

    try:
        with open(config['status_file'], "w") as f:
            f.write(new_status)
    except Exception as e:
        subprocess.run(["logger", f"Error writing to status file: {e}"])

# ------------------ GUI SETUP ------------------
root = tk.Tk()
if config["fullscreen"]:
    root.attributes("-fullscreen", True)

root.geometry(f"{root.winfo_screenwidth()}x{root.winfo_screenheight()}")

# Load & Resize Logo
try:
    logo_img = Image.open(config["logo_path"])
    logo_img = logo_img.resize((root.winfo_screenwidth() // 3, root.winfo_screenheight() // 6), Image.LANCZOS)
    logo = ImageTk.PhotoImage(logo_img)
except Exception as e:
    subprocess.run(["logger", f"Error loading logo: {e}"])
    logo = None

# UI Components
frame = tk.Frame(root, bg=config["available_color"] if status == "Available" else config["unavailable_color"])
frame.pack(fill="both", expand=True)

if logo:
    logo_label = tk.Label(frame, image=logo, bg=frame.cget("bg"))
    logo_label.pack(pady=20)

status_label = tk.Label(frame, text=f"PUCC {status}", font=("Arial", 50, "bold"), fg="white", bg=frame.cget("bg"))
status_label.pack(pady=20)

countdown_label = tk.Label(frame, text="", font=("Arial", 30), fg="white", bg=frame.cget("bg"))
countdown_label.pack()

# ------------------ UI UPDATE FUNCTION ------------------
def update_ui():
    """Updates UI components to reflect current status."""
    frame.config(bg=config["available_color"] if status == "Available" else config["unavailable_color"])
    status_label.config(text=f"PUCC {status}", bg=frame.cget("bg"))
    countdown_label.config(bg=frame.cget("bg"))
    update_toggle_button()

# ------------------ BUTTON POP-UP SELECTION ------------------
def ask_reason(status_type):
    """Presents large buttons instead of dropdown for easier touchscreen use."""
    reasons = {
        "Available": ["I was notified it is available", "It was marked as unavailable in error"],
        "Unavailable": ["Not specified", "No staff", "Full", "It was marked as available in error"]
    }

    popup = tk.Toplevel(root)
    popup.title("Select Reason")
    popup.geometry("500x400")
    popup.configure(bg="white")

    tk.Label(popup, text=f"Reason for marking PUCC as {status_type}:", font=("Arial", 14, "bold"), bg="white").pack(pady=10)

    def submit_reason(reason):
        update_status(status_type, reason)
        popup.destroy()

    for reason in reasons[status_type]:
        tk.Button(popup, text=reason, font=("Arial", 16), width=30, height=2, command=lambda r=reason: submit_reason(r)).pack(pady=5)

    tk.Button(popup, text="Cancel", font=("Arial", 16), width=30, height=2, bg="red", fg="white", command=popup.destroy).pack(pady=10)

# ------------------ STATUS CHANGE ------------------
def update_countdown():
    """Updates the countdown timer every minute while PUCC is unavailable."""
    global status_end_time
    if status == "Unavailable" and status_end_time:
        time_remaining = status_end_time - datetime.now()
        if time_remaining.total_seconds() > 0:
            minutes = time_remaining.seconds // 60  # Only show minutes
            print(f"[DEBUG] Countdown updating: {minutes} min remaining")  # Debug print
            countdown_label.config(text=f"Unavailable for: {minutes} min")
            root.after(60000, update_countdown)  # Schedule next update in 60 seconds
        else:
            print("[DEBUG] Countdown finished, switching PUCC to Available")  # Debug print
            update_status("Available", "Auto-reset after countdown")
    else:
        countdown_label.config(text="")  # Clear countdown if PUCC is available


def update_status(new_status, reason=""):
    """Updates status and triggers UI update."""
    global status, status_end_time

    prev_status = status
    status = new_status
    log_status_change(prev_status, new_status, reason)
    update_ui()

    if new_status == "Unavailable": 
        status_end_time = datetime.now() + timedelta(hours=1)  # Set end time for countdown
        update_countdown()  # Start countdown timer
    else:
        status_end_time = None  # Reset the timer
        countdown_label.config(text="")  # ❗ Clear the countdown immediately



# Update button text dynamically
def update_toggle_button():
    if status == "Available":
        toggle_button.config(text="Mark Unavailable", command=lambda: ask_reason("Unavailable"))
    else:
        toggle_button.config(text="Mark Available", command=lambda: ask_reason("Available"))

# Create the toggle button
toggle_button = tk.Button(frame, font=("Arial", 30, "bold"), width=15, height=2, bg=config["button_color"], fg="white")
toggle_button.pack(pady=30)
update_toggle_button()

update_ui()
root.mainloop()
