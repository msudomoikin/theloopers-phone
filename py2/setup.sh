#!/bin/bash
# Quick Setup Script for Looperphone
# Run this after copying files to Raspberry Pi

echo "=== Looperphone Quick Setup ==="

# Make scripts executable
chmod +x install.sh
chmod +x run.py
chmod +x simple_test.py
chmod +x config.py

# Create necessary directories
mkdir -p logs
mkdir -p audio

echo "Basic setup complete!"
echo ""
echo "Next steps:"
echo "1. Run: sudo ./install.sh"
echo "2. Reboot: sudo reboot"  
echo "3. Test: python3 config.py test"
echo "4. Run: python3 run.py"
