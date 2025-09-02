#!/bin/bash
# Installation script for Looperphone on Raspberry Pi
# Run as: sudo ./install.sh

echo "=== Looperphone Installation Script ==="

# Update system
echo "Updating system packages..."
apt update && apt upgrade -y

# Install system dependencies
echo "Installing system dependencies..."
apt install -y python3-pip mpg123 i2c-tools

# Enable I2C interface
echo "Enabling I2C interface..."
raspi-config nonint do_i2c 0

# Install Python dependencies
echo "Installing Python packages..."
pip3 install -r requirements.txt

# Create audio directory
echo "Creating audio directory..."
mkdir -p audio

# Set permissions for GPIO access
echo "Setting up GPIO permissions..."
usermod -a -G gpio $SUDO_USER

# Create systemd service for autostart (optional)
echo "Creating systemd service..."
cat > /etc/systemd/system/looperphone.service << EOF
[Unit]
Description=Looperphone Service
After=multi-user.target

[Service]
Type=idle
User=pi
ExecStart=/usr/bin/python3 /home/pi/looperphone/main.py
WorkingDirectory=/home/pi/looperphone
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
EOF

# Enable service (commented out by default)
# systemctl enable looperphone.service

echo ""
echo "=== Installation Complete ==="
echo "1. Reboot the Raspberry Pi: sudo reboot"
echo "2. Test I2C connection: i2cdetect -y 1"
echo "3. Run the application: python3 main.py"
echo ""
echo "Optional: Enable autostart service with:"
echo "sudo systemctl enable looperphone.service"
