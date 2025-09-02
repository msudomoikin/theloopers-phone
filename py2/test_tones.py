#!/usr/bin/env python3
"""
Test script for new tone logic
Tests idle tone and DTMF key tones
"""
import time
import sys
from tones import ToneGenerator
from keypad_control import KeypadController

def test_idle_tone():
    """Test continuous idle tone"""
    print("Testing idle tone (should play continuously)...")
    tones = ToneGenerator()
    
    try:
        tones.start_continuous_tone(440)  # 440Hz Russian dial tone
        print("Idle tone started. Press Ctrl+C to stop.")
        
        # Let it play for a while
        time.sleep(5)
        
    except KeyboardInterrupt:
        pass
    finally:
        tones.stop_continuous_tone()
        tones.cleanup()
        print("Idle tone test completed")

def test_key_tones():
    """Test DTMF key tone logic"""
    print("Testing DTMF key tones...")
    print("This test simulates key press/release without actual GPIO")
    
    tones = ToneGenerator() 
    keypad = KeypadController()
    keypad.set_tone_generator(tones)
    
    try:
        # Start idle tone
        print("Starting idle tone...")
        tones.start_continuous_tone(440)
        time.sleep(2)
        
        # Simulate key press
        print("Simulating key '5' press...")
        keypad.start_key_tone('5')
        time.sleep(1)
        
        # Simulate key release
        print("Simulating key release...")
        keypad.stop_key_tone()
        
        # Restart idle tone
        print("Restarting idle tone...")
        tones.start_continuous_tone(440)
        time.sleep(1)
        
        # Test another key
        print("Simulating key '9' press...")
        keypad.start_key_tone('9')
        time.sleep(1)
        
        print("Simulating key release...")
        keypad.stop_key_tone()
        
    except KeyboardInterrupt:
        pass
    finally:
        keypad.cleanup()
        tones.cleanup()
        print("DTMF key tone test completed")

def main():
    print("=== Tone Logic Test ===")
    
    if len(sys.argv) < 2:
        print("Usage: python3 test_tones.py [idle|keys|all]")
        return
    
    test_type = sys.argv[1].lower()
    
    if test_type == "idle":
        test_idle_tone()
    elif test_type == "keys":
        test_key_tones()
    elif test_type == "all":
        print("Running all tone tests...")
        test_idle_tone()
        time.sleep(1)
        test_key_tones()
    else:
        print("Unknown test type. Use: idle, keys, or all")

if __name__ == "__main__":
    main()
