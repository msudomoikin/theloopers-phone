#!/usr/bin/env python3
"""
Configuration and Setup Utility for Looperphone
"""
import os
import subprocess
import sys

class LooperphoneConfig:
    def __init__(self):
        self.config_file = "looperphone.conf"
    
    def check_i2c(self):
        """Check I2C configuration"""
        print("Checking I2C configuration...")
        
        try:
            # Check if I2C is enabled
            result = subprocess.run(['i2cdetect', '-y', '1'], 
                                  capture_output=True, text=True)
            
            if "27" in result.stdout:
                print("✓ LCD found at address 0x27")
                return True
            else:
                print("✗ LCD not found at address 0x27")
                print("Check connections and I2C configuration")
                return False
                
        except FileNotFoundError:
            print("✗ i2c-tools not installed")
            print("Install with: sudo apt-get install i2c-tools")
            return False
    
    def check_audio(self):
        """Check audio configuration"""
        print("Checking audio configuration...")
        
        try:
            # Test audio output
            result = subprocess.run(['aplay', '/usr/share/sounds/alsa/Front_Left.wav'], 
                                  capture_output=True, text=True, timeout=5)
            
            if result.returncode == 0:
                print("✓ Audio output working")
                return True
            else:
                print("✗ Audio output issue")
                return False
                
        except (FileNotFoundError, subprocess.TimeoutExpired):
            print("? Audio test skipped (no test file or timeout)")
            return None
    
    def check_gpio_permissions(self):
        """Check GPIO access permissions"""
        print("Checking GPIO permissions...")
        
        try:
            import RPi.GPIO as GPIO
            GPIO.setmode(GPIO.BCM)
            GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_UP)
            GPIO.cleanup()
            print("✓ GPIO access working")
            return True
            
        except ImportError:
            print("✗ RPi.GPIO not installed")
            return False
        except Exception as e:
            print(f"✗ GPIO access denied: {e}")
            print("Add user to gpio group: sudo usermod -a -G gpio $USER")
            return False
    
    def check_dependencies(self):
        """Check Python dependencies"""
        print("Checking Python dependencies...")
        
        dependencies = [
            'sounddevice', 'numpy', 'RPLCD', 'smbus2', 'RPi.GPIO'
        ]
        
        missing = []
        for dep in dependencies:
            try:
                __import__(dep)
                print(f"✓ {dep}")
            except ImportError:
                print(f"✗ {dep}")
                missing.append(dep)
        
        if missing:
            print(f"\nInstall missing packages with:")
            print(f"pip3 install {' '.join(missing)}")
            return False
        
        return True
    
    def check_system_packages(self):
        """Check system packages"""
        print("Checking system packages...")
        
        packages = ['mpg123']
        missing = []
        
        for package in packages:
            try:
                subprocess.run([package, '--version'], 
                             capture_output=True, check=True)
                print(f"✓ {package}")
            except (subprocess.CalledProcessError, FileNotFoundError):
                print(f"✗ {package}")
                missing.append(package)
        
        if missing:
            print(f"\nInstall missing packages with:")
            print(f"sudo apt-get install {' '.join(missing)}")
            return False
        
        return True
    
    def create_audio_directory(self):
        """Create audio directory structure"""
        print("Setting up audio directory...")
        
        os.makedirs('audio', exist_ok=True)
        
        # Create sample files list
        countries = [
            'russia', 'canada', 'australia', 'japan', 'india',
            'austria', 'serbia', 'guinea', 'pakistan'
        ]
        
        print("Audio directory created. Add these MP3 files:")
        for country in countries:
            print(f"  - {country}.mp3")
        
        return True
    
    def run_diagnostics(self):
        """Run full system diagnostics"""
        print("=== Looperphone System Diagnostics ===\n")
        
        checks = [
            ("Python Dependencies", self.check_dependencies),
            ("System Packages", self.check_system_packages),
            ("GPIO Permissions", self.check_gpio_permissions),
            ("I2C LCD", self.check_i2c),
            ("Audio Output", self.check_audio),
            ("Audio Directory", self.create_audio_directory),
        ]
        
        results = []
        for name, check_func in checks:
            print(f"\n--- {name} ---")
            result = check_func()
            results.append((name, result))
        
        # Summary
        print("\n=== Diagnostic Summary ===")
        passed = 0
        total = len([r for r in results if r[1] is not None])
        
        for name, result in results:
            if result is True:
                print(f"✓ {name}")
                passed += 1
            elif result is False:
                print(f"✗ {name}")
            else:
                print(f"? {name} (skipped)")
        
        print(f"\nPassed: {passed}/{total}")
        
        if passed == total:
            print("System ready for operation!")
            return True
        else:
            print("Some issues found. Address them before running main.py")
            return False

def main():
    if len(sys.argv) > 1:
        if sys.argv[1] == "test":
            config = LooperphoneConfig()
            config.run_diagnostics()
        else:
            print("Usage: python3 config.py [test]")
    else:
        print("Looperphone Configuration Utility")
        print("Run 'python3 config.py test' for system diagnostics")

if __name__ == "__main__":
    main()
