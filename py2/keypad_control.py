"""
Keypad Controller for Looperphone
Handles matrix keypad input with DTMF tone generation
"""
import time
import RPi.GPIO as GPIO
import sounddevice as sd
import numpy as np

# Keypad matrix configuration
ROWS = [0, 5, 6, 13]      # GPIO pins for rows
COLS = [17, 27, 22]       # GPIO pins for columns

# Keypad layout
KEYMAP = [
    ['1', '2', '3'],
    ['4', '5', '6'], 
    ['7', '8', '9'],
    ['*', '0', '#']
]

# DTMF frequencies (Hz)
DTMF_TONES = {
    "1": (697, 1209), "2": (697, 1336), "3": (697, 1477),
    "4": (770, 1209), "5": (770, 1336), "6": (770, 1477),
    "7": (852, 1209), "8": (852, 1336), "9": (852, 1477),
    "*": (941, 1209), "0": (941, 1336), "#": (941, 1477)
}

class KeypadController:
    def __init__(self, sample_rate=44100):
        """Initialize keypad and audio"""
        self.sample_rate = sample_rate
        self.current_tone_thread = None
        self.stop_tone = False
        
        # Setup GPIO for keypad
        GPIO.setmode(GPIO.BCM)
        
        # Setup row pins as inputs with pull-up
        for row_pin in ROWS:
            GPIO.setup(row_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        
        # Setup column pins as outputs
        for col_pin in COLS:
            GPIO.setup(col_pin, GPIO.OUT)
            GPIO.output(col_pin, GPIO.HIGH)
        
        print("Keypad controller initialized")
    
    def generate_dtmf_tone(self, freq1, freq2, duration=0.2):
        """Generate DTMF tone with two frequencies"""
        try:
            t = np.linspace(0, duration, int(self.sample_rate * duration))
            tone1 = np.sin(2 * np.pi * freq1 * t)
            tone2 = np.sin(2 * np.pi * freq2 * t)
            combined = (tone1 + tone2) * 0.3  # Reduce volume
            
            sd.play(combined, self.sample_rate)
            
        except Exception as e:
            print(f"DTMF tone error: {e}")
    
    def play_key_tone(self, key):
        """Play DTMF tone for pressed key"""
        if key in DTMF_TONES:
            freq1, freq2 = DTMF_TONES[key]
            self.generate_dtmf_tone(freq1, freq2)
    
    def scan_keypad(self):
        """Scan keypad for pressed key"""
        for col_index, col_pin in enumerate(COLS):
            # Set current column low
            GPIO.output(col_pin, GPIO.LOW)
            
            # Check all rows
            for row_index, row_pin in enumerate(ROWS):
                if GPIO.input(row_pin) == GPIO.LOW:
                    key = KEYMAP[row_index][col_index]
                    
                    # Wait for key release to avoid multiple presses
                    while GPIO.input(row_pin) == GPIO.LOW:
                        time.sleep(0.01)
                    
                    # Reset column
                    GPIO.output(col_pin, GPIO.HIGH)
                    return key
            
            # Reset column
            GPIO.output(col_pin, GPIO.HIGH)
        
        return None
    
    def get_code(self, timeout=3):
        """Get country code input with timeout"""
        code = ""
        start_time = time.time()
        last_key_time = start_time
        
        print(f"Waiting for country code (timeout: {timeout}s)")
        
        while True:
            # Check for timeout
            current_time = time.time()
            if current_time - last_key_time > timeout:
                print(f"Input timeout, code entered: '{code}'")
                break
            
            # Scan for key press
            key = self.scan_keypad()
            
            if key and key.isdigit():  # Only accept digits
                code += key
                last_key_time = current_time
                
                # Play DTMF tone for the key
                self.play_key_tone(key)
                
                print(f"Key pressed: {key}, current code: {code}")
                
                # Update display would be handled by main loop
                
            time.sleep(0.05)  # Small delay to prevent CPU overload
        
        return code if code else None
    
    def cleanup(self):
        """Clean up keypad resources"""
        # Stop any ongoing tones
        sd.stop()
        print("Keypad cleanup completed")
