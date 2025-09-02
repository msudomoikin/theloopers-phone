#!/usr/bin/env python3
"""
Looperphone Launcher with Logging and Error Handling
Production launcher for the payphone system
"""
import logging
import sys
import os
import time
from datetime import datetime

# Setup logging
def setup_logging():
    """Configure logging for the system"""
    log_dir = "logs"
    os.makedirs(log_dir, exist_ok=True)
    
    log_file = os.path.join(log_dir, f"looperphone_{datetime.now().strftime('%Y%m%d')}.log")
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler(sys.stdout)
        ]
    )
    
    return logging.getLogger('Looperphone')

def check_system_ready():
    """Quick system readiness check"""
    checks = []
    
    # Check if running on Raspberry Pi
    try:
        with open('/proc/cpuinfo', 'r') as f:
            if 'Raspberry Pi' in f.read():
                checks.append(("Raspberry Pi", True))
            else:
                checks.append(("Raspberry Pi", False))
    except:
        checks.append(("Raspberry Pi", False))
    
    # Check critical imports
    critical_modules = ['RPi.GPIO', 'sounddevice', 'numpy', 'RPLCD.i2c']
    for module in critical_modules:
        try:
            __import__(module)
            checks.append((module, True))
        except ImportError:
            checks.append((module, False))
    
    # Report results
    all_good = True
    for name, status in checks:
        if status:
            print(f"✓ {name}")
        else:
            print(f"✗ {name}")
            all_good = False
    
    return all_good

def main():
    """Main launcher function"""
    print("=== Looperphone System Starting ===")
    print(f"Start time: {datetime.now()}")
    
    # Setup logging
    logger = setup_logging()
    logger.info("Looperphone system starting")
    
    # Check system readiness
    if not check_system_ready():
        print("\nSystem not ready. Run 'python3 config.py test' for diagnostics.")
        logger.error("System readiness check failed")
        return 1
    
    print("\nSystem checks passed. Starting main application...")
    logger.info("System checks passed, starting main application")
    
    # Import and start main application
    try:
        from main import LooperPhone
        
        # Create and run the phone system
        phone = LooperPhone()
        logger.info("LooperPhone instance created successfully")
        
        print("Looperphone is now running...")
        print("Press Ctrl+C to stop\n")
        
        phone.run()
        
    except KeyboardInterrupt:
        print("\n\nShutdown requested by user")
        logger.info("Shutdown requested by user (Ctrl+C)")
        
    except Exception as e:
        print(f"\nCritical error: {e}")
        logger.error(f"Critical error in main application: {e}", exc_info=True)
        return 1
    
    finally:
        logger.info("Looperphone system stopped")
        print("Looperphone system stopped")
    
    return 0

if __name__ == "__main__":
    try:
        exit_code = main()
        sys.exit(exit_code)
    except Exception as e:
        print(f"Launcher error: {e}")
        sys.exit(1)
