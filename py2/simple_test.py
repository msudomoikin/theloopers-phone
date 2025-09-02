#!/usr/bin/env python3
"""
Simple Component Tester for Looperphone
Quick tests for individual components
"""
import sys
import time

def test_lcd_simple():
    """Simple LCD test"""
    print("Testing LCD...")
    try:
        from RPLCD.i2c import CharLCD
        lcd = CharLCD('PCF8574', 0x27)
        lcd.clear()
        lcd.write_string("Looperphone")
        lcd.cursor_pos = (1, 0)
        lcd.write_string("LCD Working!")
        
        time.sleep(3)
        lcd.clear()
        lcd.close(clear=True)
        print("LCD test: PASS")
        return True
    except Exception as e:
        print(f"LCD test: FAIL - {e}")
        return False

def test_keypad_simple():
    """Simple keypad test"""
    print("Testing keypad... Press any key within 5 seconds")
    try:
        import RPi.GPIO as GPIO
        
        ROWS = [0, 5, 6, 13]
        COLS = [17, 27, 22]
        KEYMAP = [['1', '2', '3'], ['4', '5', '6'], ['7', '8', '9'], ['*', '0', '#']]
        
        GPIO.setmode(GPIO.BCM)
        for row_pin in ROWS:
            GPIO.setup(row_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        for col_pin in COLS:
            GPIO.setup(col_pin, GPIO.OUT)
            GPIO.output(col_pin, GPIO.HIGH)
        
        start_time = time.time()
        key_found = False
        
        while time.time() - start_time < 5:
            for col_index, col_pin in enumerate(COLS):
                GPIO.output(col_pin, GPIO.LOW)
                for row_index, row_pin in enumerate(ROWS):
                    if GPIO.input(row_pin) == GPIO.LOW:
                        key = KEYMAP[row_index][col_index]
                        print(f"Key pressed: {key}")
                        key_found = True
                        break
                GPIO.output(col_pin, GPIO.HIGH)
                if key_found:
                    break
            if key_found:
                break
            time.sleep(0.1)
        
        GPIO.cleanup()
        
        if key_found:
            print("Keypad test: PASS")
            return True
        else:
            print("Keypad test: TIMEOUT (no key pressed)")
            return False
            
    except Exception as e:
        print(f"Keypad test: FAIL - {e}")
        return False

def test_hook_switch():
    """Test hook switch"""
    print("Testing hook switch... Pick up/hang up phone within 5 seconds")
    try:
        import RPi.GPIO as GPIO
        
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        
        start_time = time.time()
        initial_state = GPIO.input(23)
        print(f"Initial hook state: {'ON HOOK' if initial_state == GPIO.HIGH else 'OFF HOOK'}")
        
        state_changed = False
        while time.time() - start_time < 5:
            current_state = GPIO.input(23)
            if current_state != initial_state:
                print(f"Hook state changed: {'ON HOOK' if current_state == GPIO.HIGH else 'OFF HOOK'}")
                state_changed = True
                break
            time.sleep(0.1)
        
        GPIO.cleanup()
        
        if state_changed:
            print("Hook switch test: PASS")
            return True
        else:
            print("Hook switch test: TIMEOUT (no state change)")
            return False
            
    except Exception as e:
        print(f"Hook switch test: FAIL - {e}")
        return False

def test_audio_simple():
    """Simple audio test"""
    print("Testing audio (you should hear a beep)...")
    try:
        import sounddevice as sd
        import numpy as np
        
        # Generate 1 second 440Hz tone
        sample_rate = 44100
        t = np.linspace(0, 1, sample_rate)
        tone = np.sin(2 * np.pi * 440 * t) * 0.3
        
        sd.play(tone, sample_rate)
        sd.wait()
        
        print("Audio test: PASS (if you heard a beep)")
        return True
        
    except Exception as e:
        print(f"Audio test: FAIL - {e}")
        return False

def main():
    """Run selected tests"""
    if len(sys.argv) < 2:
        print("Usage: python3 simple_test.py [lcd|keypad|hook|audio|all]")
        return
    
    test_type = sys.argv[1].lower()
    
    if test_type == "lcd":
        test_lcd_simple()
    elif test_type == "keypad":
        test_keypad_simple()
    elif test_type == "hook":
        test_hook_switch()
    elif test_type == "audio":
        test_audio_simple()
    elif test_type == "all":
        print("=== Running All Simple Tests ===\n")
        tests = [
            ("LCD", test_lcd_simple),
            ("Audio", test_audio_simple),
            ("Hook Switch", test_hook_switch),
            ("Keypad", test_keypad_simple),
        ]
        
        passed = 0
        for name, test_func in tests:
            print(f"\n--- {name} ---")
            if test_func():
                passed += 1
        
        print(f"\n=== Results: {passed}/{len(tests)} tests passed ===")
    else:
        print("Unknown test type. Use: lcd, keypad, hook, audio, or all")

if __name__ == "__main__":
    main()
