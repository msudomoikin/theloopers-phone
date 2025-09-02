#!/usr/bin/env python3
"""
Looperphone - Raspberry Pi Payphone System
Main loop: monitors hook switch, manages call flow
"""
import time
import RPi.GPIO as GPIO
from lcd_control import LCDController
from keypad_control import KeypadController  
from tones import ToneGenerator
from audio_player import AudioPlayer
from countries import get_country_info

# GPIO Configuration
HOOK_PIN = 23  # Hook switch (GPIO23 to GND)

# Timeout Configuration
COUNTRY_CODE_TIMEOUT = 5  # Timeout in seconds for country code input

class LooperPhone:
    def __init__(self):
        # Initialize components
        self.lcd = LCDController()
        self.keypad = KeypadController()
        self.tones = ToneGenerator()
        self.audio = AudioPlayer()
        
        # Link keypad to tone generator for idle tone management
        self.keypad.set_tone_generator(self.tones)
        
        # Setup GPIO for hook switch
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(HOOK_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        
        print("Looperphone initialized")
    
    def is_hook_off(self):
        """Check if phone is picked up (GPIO23 connected to GND)"""
        return GPIO.input(HOOK_PIN) == GPIO.LOW
    
    def wait_for_pickup(self):
        """Wait for phone to be picked up"""
        self.lcd.show_message("Pick up the", "phone")
        
        while not self.is_hook_off():
            time.sleep(0.1)
        
        print("Phone picked up")
    
    def handle_call(self):
        """Main call handling logic"""
        try:
            # Show dial tone message (idle tone will be started by keypad)
            self.lcd.show_message("Enter country", "code")
            
            # Get country code with timeout (keypad manages idle tone internally and updates LCD)
            country_code = self.keypad.get_code(
                timeout=COUNTRY_CODE_TIMEOUT, 
                hook_check_func=self.is_hook_off,
                lcd_controller=self.lcd
            )
            
            # Always stop any tones when exiting get_code
            self.keypad.stop_any_tone()
            self.tones.stop_continuous_tone()  # Ensure idle tone is stopped
            
            if not country_code:
                self.lcd.show_message("Timeout", "Hanging up...")
                time.sleep(2)
                return
            
            # Get country info
            country_info = get_country_info(country_code)
            country_name = country_info['name']
            
            # Display country name
            self.lcd.show_message("Calling:", country_name[:16])
            print(f"Calling {country_name} (+{country_code})")
            
            # Ensure no keypad tones are playing
            self.keypad.stop_any_tone()
            # Generate country-specific dial tone for 10 seconds
            dial_params = country_info['dial_tone']
            self.tones.generate_dial_tone(dial_params, duration=10)
            
            # Check if still on hook during dialing
            if not self.is_hook_off():
                return
            
            # Play country mp3 file
            self.audio.play_country_file(country_name.lower())
            
            # Ensure no keypad tones are playing
            self.keypad.stop_any_tone()
            # Generate busy tone
            busy_params = country_info['busy_tone']
            self.tones.generate_busy_tone(busy_params)
            
        except Exception as e:
            print(f"Error during call: {e}")
            # Stop all tones in case of error
            self.keypad.stop_any_tone()
            self.tones.stop_continuous_tone()
            self.lcd.show_message("Error", "Please hang up")
            time.sleep(2)
        finally:
            # Always stop all tones when call handling ends
            self.keypad.stop_any_tone()
            self.tones.stop_continuous_tone()
    
    def run(self):
        """Main loop"""
        print("Starting Looperphone...")
        
        try:
            while True:
                # Wait for pickup
                self.wait_for_pickup()
                
                # Handle the call
                self.handle_call()
                
                # Wait for hangup
                while self.is_hook_off():
                    time.sleep(0.1)
                
                # Stop all tones and clear display after hangup
                self.keypad.stop_any_tone()
                self.tones.stop_continuous_tone()
                self.lcd.clear()
                print("Call ended, phone hung up")
                time.sleep(0.5)
                
        except KeyboardInterrupt:
            print("\nShutting down...")
        finally:
            self.cleanup()
    
    def cleanup(self):
        """Clean up resources"""
        self.keypad.cleanup()
        self.tones.cleanup()
        self.lcd.cleanup()
        GPIO.cleanup()
        print("Cleanup completed")

if __name__ == "__main__":
    phone = LooperPhone()
    phone.run()
