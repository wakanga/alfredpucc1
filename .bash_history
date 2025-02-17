xhost +SI:localuser:alfredpi1
alfredpi1@raspberrypi:~ $ xhost +SI:localuser:alfredpi1
xhost:  unable to open display ""
alfredpi1@raspberrypi:~ $
export DISPLAY=:0
python3 /home/alfredpi1/pucc_status.py
ssh alfredpi1@<your_raspberry_pi_ip_address>
pkill -f "python3 /home/alfredpi1/pucc_status.py"
exit
journalctl -u pucc_status.service --no-pager --lines=30
sudo nano /etc/systemd/system/pucc_status.service
sudo systemctl daemon-reload
sudo systemctl restart pucc_status.service
sudo systemctl status pucc_status.service
export DISPLAY=:0
python3 /home/alfredpi1/pucc_status.py
xhost +SI:localuser:alfredpi1
echo 'xhost +SI:localuser:alfredpi1' >> ~/.bashrc
source ~/.bashrc
sudo nano /etc/systemd/system/pucc_status.service
ls -ld /run/user/1000
sudo nano /etc/systemd/system/pucc_status.service
ls /run/user/
sudo systemctl daemon-reload
sudo systemctl restart pucc_status.service
sudo nano /etc/systemd/system/pucc_status.service
sudo systemctl daemon-reload
sudo systemctl restart pucc_status.service
sudo systemctl status pucc_status.service
sudo reboot
pkill -f "python3 /home/alfredpi1/pucc_status.py



sudo apt update && sudo apt upgrade -y
sudo apt install python3-pip python3-tk python3-pil -y
pip3 install pyyaml pillow
sudo apt update
sudo apt install python3-yaml python3-pil
chmod +x /home/alfredpi1/pucc_status.py
sudo nano /etc/systemd/system/pucc_status.service
sudo systemctl enable pucc_status.service
sudo systemctl start pucc_status.service
sudo systemctl status pucc_status.service
nano /home/alfredpi1/pucc_status.py
sudo systemctl restart pucc_status.service
sudo reboot 
sudo systemctl is-enabled pucc_status.service
sudo systemctl status pucc_status.service
journalctl -u pucc_status.service --no-pager --lines=30
pip3 uninstall pillow -y
sudo apt remove python3-pil -y
sudo apt install python3-pil python3-pil.imagetk -y
sudo reboot
nano /home/alfredpi1/pucc_status.py
sudo systemctl restart pucc_status.service
cat /home/alfredpi1/pucc_status.txt
sudo systemctl status pucc_status.service
echo $DISPLAY
xhost +SI:localuser:alfredpi1
sudo systemctl restart pucc_status.service
sudo systemctl status pucc_status.service
nano ~/.bashrc
sudo systemctl restart pucc_status.service
/usr/bin/python3 /home/alfredpi1/pucc_status.py
echo $DISPLAY
sudo nano /etc/systemd/system/pucc_status.service
sudo systemctl daemon-reload
sudo systemctl restart pucc_status.service
sudo systemctl status pucc_status.service
ps aux | grep python
sudo systemctl status pucc_status.service
nano /home/alfredpi1/pucc_config.yaml
sudo systemctl daemon-reload
sudo systemctl restart pucc_status.service
sudo systemctl status pucc_status.service
journalctl -u pucc_status.service --no-pager --lines=30
nano /home/alfredpi1/pucc_config.yaml
sudo systemctl daemon-reload
sudo systemctl restart pucc_status.service
sudo systemctl daemon-reload
sudo systemctl restart pucc_status.service
sudo systemctl daemon-reload
sudo systemctl restart pucc_status.service
sudo systemctl daemon-reload
sudo systemctl restart pucc_status.service
sudo systemctl daemon-reload
sudo systemctl restart pucc_status.service
sudo systemctl daemon-reload
sudo systemctl restart pucc_status.service
sudo systemctl daemon-reload
sudo systemctl restart pucc_status.service
sudo shutdown
pucc_status
sudo systemctl stop pucc_status.service
/usr/bin/python3 /home/alfredpi1/pucc_status.py
sudo systemctl daemon-reload
sudo systemctl restart pucc_status.service
sudo systemctl daemon-reload
sudo systemctl restart pucc_status.service
sudo systemctl daemon-reload
sudo systemctl restart pucc_status.service
sudo shutdown now
sudo
sudo systemctl restart pucc_status.service
sudo reboot now
cat /home/alfredpi1/pucc_status.txt
[200~sudo systemctl restart pucc_status.service~
sudo systemctl restart pucc_status.service
sudo systemctl status pucc_status.service
journalctl -u pucc_status.service -n 20 -f
ps aux | grep python
journalctl -u pucc_status.service --no-pager --lines=30
/usr/bin/python3 /home/alfredpi1/pucc_status.py
sudo systemctl restart pucc_status.service
journalctl -u pucc_status.service --no-pager --lines=20
sudo systemctl restart pucc_status.service
cd /home/alfredpi1/
# Initialize Git repository (only do this once)
git init
# Add the necessary files
git add pucc_status.py pucc_config.yaml logs/ Alfred_Emergency_Logo.jpg
# Commit with a message
git commit -m "Backup of PUCC System on $(date +'%Y-%m-%d')"
# Add GitHub as remote repository
git remote add origin <your-repository-url>
# Push changes to GitHub
git push -u origin main
cd /home/alfredpi1/
# Initialize Git repository (only do this once)
git init
# Add the necessary files
git add pucc_status.py pucc_config.yaml logs/ Alfred_Emergency_Logo.jpg
# Commit with a message
git commit -m "Backup of PUCC System on $(date +'%Y-%m-%d')"
# Add GitHub as remote repository
git remote add origin https://github.com/wakanga/alfredpucc1
# Push changes to GitHub
git push -u origin main
cd /home/alfredpi1/
# Initialize Git repository (only do this once)
git init
# Add the necessary files
git add pucc_status.py pucc_config.yaml logs/ Alfred_Emergency_Logo.jpg
# Commit with a message
git commit -m "Backup of PUCC System on $(date +'%Y-%m-%d')"
# Add GitHub as remote repository (only needed once)
git remote add origin https://github.com/wakanga/alfredpucc1
# Ensure we are on the correct branch (creates 'main' if it doesn't exist)
git branch -M main
# Push changes to GitHub (force sets upstream branch)
git push -u origin main
git config --global user.name "wakanga"
git config --global user.email "GitHub"kanga.addy.io"



