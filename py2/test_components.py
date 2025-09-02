#!/usr/bin/env python3
"""
Test script for Looperphone components
Tests each component individually for debugging
"""
import time
import sys
import os

# Add current directory to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_lcd():
    """Test LCD display"""
    print("Testing LCD Display...")
    try:
        from lcd_control import LCDController
        lcd = LCDController()
        
        lcd.show_message("LCD Test", "Working!")
        time.sleep(3)
        
        lcd.show_message("Line 1 Test", "Line 2 Test")
        time.sleep(3)
        
        lcd.clear()
        print("LCD test completed successfully")
        return True
        
    except Exception as e:
        print(f"LCD test failed: {e}")
        return False

def test_keypad():
    """Test keypad input"""
    print("Testing Keypad... Press some keys (timeout: 10s)")
    try:
        from keypad_control import KeypadController
        keypad = KeypadController()
        
        start_time = time.time()
        while time.time() - start_time < 10:
            key = keypad.scan_keypad()
            if key:
                print(f"Key pressed: {key}")
                keypad.play_key_tone(key)
                time.sleep(0.5)  # Debounce
        
        keypad.cleanup()
        print("Keypad test completed")
        return True
        
    except Exception as e:
        print(f"Keypad test failed: {e}")
        return False

def test_tones():
    """Test tone generation"""
    print("Testing Tone Generation...")
    try:
        from tones import ToneGenerator
        tones = ToneGenerator()
        
        # Test simple tone
        print("Playing 440Hz tone...")
        tone_data = tones.generate_tone(440, 1.0)
        
        # Test dual tone
        print("Playing dual tone (440+480Hz)...")
        dual_tone = tones.generate_dual_tone(440, 480, 1.0)
        
        # Test AM modulated tone
        print("Playing AM modulated tone...")
        am_tone = tones.generate_am_modulated_tone(425, 25, 1.0)
        
        tones.cleanup()
        print("Tone test completed")
        return True
        
    except Exception as e:
        print(f"Tone test failed: {e}")
        return False

def test_audio():
    """Test audio playback"""
    print("Testing Audio Playback...")
    try:
        from audio_player import AudioPlayer
        audio = AudioPlayer()
        
        # Create test audio directory
        os.makedirs("audio", exist_ok=True)
        
        # Try to play a test file (will fail gracefully if not found)
        audio.play_country_file("test")
        
        audio.cleanup()
        print("Audio test completed")
        return True
        
    except Exception as e:
        print(f"Audio test failed: {e}")
        return False

def test_countries():
    """Test country database"""
    print("Testing Country Database...")
    try:
        from countries import get_country_info, list_supported_countries
        
        # List all countries
        list_supported_countries()
        
        # Test some lookups
        russia = get_country_info("7")
        print(f"\nRussia info: {russia['name']}")
        
        unknown = get_country_info("999")
        print(f"Unknown country: {unknown['name']}")
        
        print("Country database test completed")
        return True
        
    except Exception as e:
        print(f"Country test failed: {e}")
        return False

def test_gpio():
    """Test GPIO setup"""
    print("Testing GPIO Setup...")
    try:
        import RPi.GPIO as GPIO
        
        # Test hook pin
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        
        hook_state = GPIO.input(23)
        print(f"Hook switch state: {'OFF HOOK' if hook_state == GPIO.LOW else 'ON HOOK'}")
        
        GPIO.cleanup()
        print("GPIO test completed")
        return True
        
    except Exception as e:
        print(f"GPIO test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("=== Looperphone Component Tests ===\n")
    
    tests = [
        ("Countries", test_countries),
        ("GPIO", test_gpio),
        ("LCD", test_lcd),
        ("Tones", test_tones),
        ("Audio", test_audio),
        ("Keypad", test_keypad),
    ]
    
    results = {}
    
    for test_name, test_func in tests:
        print(f"\n--- {test_name} Test ---")
        results[test_name] = test_func()
        print()
    
    # Summary
    print("=== Test Results ===")
    passed = 0
    total = len(tests)
    
    for test_name, result in results.items():
        status = "PASS" if result else "FAIL"
        print(f"{test_name}: {status}")
        if result:
            passed += 1
    
    print(f"\nPassed: {passed}/{total}")
    
    if passed == total:
        print("All tests passed! System ready.")
    else:
        print("Some tests failed. Check hardware connections and dependencies.")

if __name__ == "__main__":
    main()
