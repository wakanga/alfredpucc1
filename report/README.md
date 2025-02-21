# PUCC Availability System - Blueprint Document

## 1. Introduction
### Project Name: PUCC Availability System

### Purpose
Provides a clear, real-time status indicator for the Prahran Medicare Urgent Care Clinic (PUCC) within the Emergency Department. It reduces manual communication by displaying whether PUCC is accepting patients.

### Intended Users
- Emergency Department staff
- PUCC staff

### Core Functionalities
- Full-Screen Touch UI displaying PUCC status
- Green (Available) / Red (Unavailable) indicators
- Manual Toggle with reason selection (large button interface)
- Automatic 'Unavailable' switch at 21:00 (configurable)
- Countdown timer when PUCC is unavailable (updates every minute)
- Comprehensive logging of all status changes, including reasons
- Stable, minimal scheduled tasks for lightweight operation
- Auto-reset after 60 minutes when PUCC is unavailable
- Automatic startup on boot

---

## 2. System Components
### Hardware Requirements
- Raspberry Pi 4 (running Raspberry Pi OS)
- 7-inch touchscreen display
- Power supply

### Software Stack
- Raspberry Pi OS
- Python 3.x

### File Structure
```
/home/alfredpi1/
├── pucc_status.py     (Main Script)
├── pucc_config.yaml   (Configuration File)
├── logs/
│   ├── pucc_logs_YYYY_MM.csv (Monthly logs)
├── Alfred_Emergency_Logo.jpg (Logo for UI)
```

---

## 3. Installation & Setup Guide
### Step 1: Prepare the Raspberry Pi
1. Flash Raspberry Pi OS onto an SD card.
2. Connect the touchscreen display.
3. Boot the Pi and complete initial setup.

### Step 2: Install Dependencies
```sh
sudo apt update && sudo apt upgrade -y
sudo apt install python3-pip -y
sudo apt install python3-pil python3-yaml -y
```

### Step 3: Transfer and Set Up Files
Upload the following files:
- `pucc_status.py`
- `pucc_config.yaml`
- `Alfred_Emergency_Logo.jpg`
- `logs/` folder

Ensure files have correct permissions:
```sh
chmod +x /home/alfredpi1/pucc_status.py
```

### Step 4: Set Up Systemd Service
Create a service file:
```sh
sudo nano /etc/systemd/system/pucc_status.service
```
Add the following content:
```
[Unit]
Description=PUCC Status Display
After=graphical.target

[Service]
User=alfredpi1  # Replace with your username
WorkingDirectory=/home/alfredpi1/
ExecStart=/usr/bin/python3 /home/alfredpi1/pucc_status.py
Restart=always
RestartSec=5
Environment=DISPLAY=:0
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
```
Enable and start the service:
```sh
sudo systemctl enable pucc_status.service
sudo systemctl start pucc_status.service
```
Check the status:
```sh
sudo systemctl status pucc_status.service
```

### Step 5: Configure `pucc_config.yaml`
Create `pucc_config.yaml`:
```yaml
logo_path: "/home/alfredpi1/Alfred_Emergency_Logo.jpg"
log_dir: "/home/alfredpi1/logs"
status_file: "/home/alfredpi1/pucc_status.txt"
available_color: "#28a745"
unavailable_color: "#dc3545"
button_color: "#007bff"
auto_unavailable_time: "21:00"
screen_off_time: "22:00"
screen_on_time: "06:00"
fullscreen: true
```

---

## 4. System Behavior & Logic
### State Machine Explanation
```
[ Available ] --Staff Tap--> [ Unavailable (Countdown Timer) ]
     ^                                       |
     | Auto-reset <--- Countdown -----> Auto-switch at 21:00
     |                                       |
     +---------------------------------------+
```

### Event Triggers
- **Manual Toggle** (Large button pop-up selection)
- **Automatic switch** to 'Unavailable' at `auto_unavailable_time`
- **Auto-reset** after countdown expiration

---

## 5. Logging & Data Handling
### Log Format
```
Timestamp, Previous Status, New Status, Reason
2025-02-16 10:05:12, Available, Unavailable, Full
2025-02-17 15:30:45, Available, Unavailable, No staff
2025-02-17 16:30:45, Unavailable, Available, Auto-reset
```
### Log Conditions
- Logs only when PUCC is marked Unavailable manually.
- Each log entry includes previous status, new status, and reason.

### Log Retrieval
- Logs can be accessed directly on the Raspberry Pi or via Pi Connect.

---

## 6. Automated Log Backup to GitHub
### Objective
Automatically commit and push only log files (`logs/*.csv`) to GitHub daily at 2 AM for secure backups.

### Configuration Steps
#### 1️⃣ Modify `.gitignore`
Ensure only the logs/ folder and .csv files are tracked.
```
*
!logs/
!logs/*.csv
```

#### 2️⃣ Set Up a cron Job
Edit crontab:
```sh
crontab -e
```
Add the following:
```sh
0 2 * * * cd /home/alfredpi1/ && git add logs/ && git commit -m "Auto Backup Logs - $(date +'%Y-%m-%d')" && git push origin main
```

#### 3️⃣ Testing & Verification
Manually test the backup:
```sh
cd /home/alfredpi1/
git add logs/
git commit -m "Manual Test Backup - $(date +'%Y-%m-%d')"
git push origin main
```
Ensure cron is active:
```sh
sudo systemctl restart cron
grep CRON /var/log/syslog
```

---

## 7. Troubleshooting & Recovery
### Common Issues & Fixes
✅ **Script doesn't start at boot**:
```sh
sudo systemctl status pucc_status.service
journalctl -u pucc_status.service --no-pager --lines=30
```
✅ **UI crashes or not displaying**:
```sh
export DISPLAY=:0 && /usr/bin/python3 /home/alfredpi1/pucc_status.py
```
✅ **To Reinstall from Scratch**:
Reflash Raspberry Pi OS and follow the setup steps above.

---

## 8. Future Roadmap
🚀 Potential Enhancements:
- Web-Based Control via Flask with REST APIs and user authentication.
- More refined logging system with staff ID (optional).
- Customizable reason selection via `pucc_config.yaml`.

---

## 9. Backup & Recovery Strategy
### Backup Using WinSCP:
1. Connect to Pi using WinSCP.
2. Download the following files:
```
/home/alfredpi1/pucc_status.py
/home/alfredpi1/pucc_config.yaml
/home/alfredpi1/logs/
/home/alfredpi1/Alfred_Emergency_Logo.jpg
```
3. Store these on your PC or upload to GitHub.

### Backup to GitHub:
```sh
git init
git add pucc_status.py pucc_config.yaml logs/ Alfred_Emergency_Logo.jpg
git commit -m "Backup of PUCC System"
git remote add origin <your-repository-url>
git push -u origin main
```

