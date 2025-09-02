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
        self.tone_generator = None
        self._mode = None  # None | 'idle' | 'key'

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
    
    def set_tone_generator(self, tone_generator):
        """Set reference to tone generator for managing idle tone"""
        self.tone_generator = tone_generator
    
    def generate_dtmf_tone(self, freq1, freq2, duration=0.2):
        """One-shot DTMF generation (blocking small beep)."""
        try:
            t = np.linspace(0, duration, int(self.sample_rate * duration))
            tone1 = np.sin(2 * np.pi * freq1 * t) * 0.3
            tone2 = np.sin(2 * np.pi * freq2 * t) * 0.3
            combined = (tone1 + tone2) / 2
            sd.play(combined, self.sample_rate)
            sd.wait()
        except Exception as e:
            print(f"DTMF tone error: {e}")

    def start_idle_tone(self, frequency=440, amplitude=0.3, length=5.0):
        """Play idle tone with shorter buffer for faster start."""
        try:
            sd.stop()
            if self.tone_generator:
                tone = self.tone_generator.generate_tone(frequency, length, amplitude)
            else:
                t = np.linspace(0, length, int(self.sample_rate * length))
                tone = np.sin(2 * np.pi * frequency * t) * amplitude
            # Use non-blocking play for immediate start
            sd.play(tone.astype(np.float32), self.sample_rate, blocking=False, loop=True)
            self._mode = 'idle'
        except Exception as e:
            print(f"Idle tone error: {e}")
    
    def start_key_tone(self, key):
        """Start DTMF tone for pressed key (plays until stop)."""
        if key in DTMF_TONES:
            freq1, freq2 = DTMF_TONES[key]
            print(f"DEBUG: Starting key tone for '{key}' ({freq1}Hz, {freq2}Hz)")
            try:
                sd.stop()
                # Use shorter buffer for faster start - 5 seconds is enough and will be stopped manually
                length = 5.0  # shorter buffer for faster generation
                if self.tone_generator:
                    tone = self.tone_generator.generate_dual_tone(freq1, freq2, length, amplitude=0.3)
                else:
                    t = np.linspace(0, length, int(self.sample_rate * length))
                    tone1 = np.sin(2 * np.pi * freq1 * t) * 0.3
                    tone2 = np.sin(2 * np.pi * freq2 * t) * 0.3
                    tone = (tone1 + tone2) / 2
                # Use non-blocking play so it starts immediately
                sd.play(tone.astype(np.float32), self.sample_rate, blocking=False)
                self._mode = 'key'
                print(f"DEBUG: Key tone started for '{key}'")
            except Exception as e:
                print(f"Key tone error: {e}")
    
    def stop_key_tone(self):
        """Stop current key tone (or any tone)."""
        print("DEBUG: Stopping key tone")
        try:
            sd.stop()
            self._mode = None
            print("DEBUG: Key tone stopped")
        except Exception as e:
            print(f"Stop key tone error: {e}")

    def stop_any_tone(self):
        """Stop any playing tone."""
        try:
            sd.stop()
            self._mode = None
        except Exception as e:
            print(f"Stop tone error: {e}")
    
    def is_key_pressed(self, key):
        """Check if specific key is currently pressed"""
        for col_index, col_pin in enumerate(COLS):
            GPIO.output(col_pin, GPIO.LOW)
            for row_index, row_pin in enumerate(ROWS):
                if GPIO.input(row_pin) == GPIO.LOW:
                    current_key = KEYMAP[row_index][col_index]
                    GPIO.output(col_pin, GPIO.HIGH)
                    return current_key == key
            GPIO.output(col_pin, GPIO.HIGH)
        return False
    
    def scan_keypad(self):
        """Scan keypad for pressed key"""
        for col_index, col_pin in enumerate(COLS):
            # Set current column low
            GPIO.output(col_pin, GPIO.LOW)
            
            # Check all rows
            for row_index, row_pin in enumerate(ROWS):
                if GPIO.input(row_pin) == GPIO.LOW:
                    key = KEYMAP[row_index][col_index]
                    # Reset column
                    GPIO.output(col_pin, GPIO.HIGH)
                    # DEBUG: Uncomment next line for debugging
                    # print(f"DEBUG: Key '{key}' detected as pressed")
                    return key
            
            # Reset column
            GPIO.output(col_pin, GPIO.HIGH)
        
        return None
    
    def get_code(self, timeout=30, hook_check_func=None, lcd_controller=None):
        """Get country code input with timeout and proper key handling"""
        code = ""
        start_time = time.time()
        last_key_time = start_time
        current_pressed_key = None
        key_start_time = None
        input_started = False  # Flag to track if user started entering code

        print(f"Waiting for country code (timeout: {timeout}s)")

        # Start idle tone only initially
        self.start_idle_tone(440)

        try:
            while True:
                # Check if phone is still off hook
                if hook_check_func and not hook_check_func():
                    print("Phone hung up during code entry")
                    self.stop_any_tone()
                    return None

                # Check for timeout
                current_time = time.time()
                if current_time - last_key_time > timeout:
                    print(f"Input timeout, code entered: '{code}'")
                    break

                # Scan for currently pressed key
                pressed_key = self.scan_keypad()

                # Handle key press/release logic
                if pressed_key and pressed_key.isdigit():
                    if pressed_key != current_pressed_key:
                        # New key pressed
                        print(f"DEBUG: New key '{pressed_key}' pressed (was: {current_pressed_key})")
                        
                        # Stop idle tone on first key press
                        if not input_started:
                            input_started = True
                            self.stop_any_tone()  # Stop idle tone
                        
                        if current_pressed_key:
                            # Stop previous key tone
                            self.stop_key_tone()

                        # Start new key tone
                        current_pressed_key = pressed_key
                        key_start_time = current_time
                        self.start_key_tone(pressed_key)
                        print(f"Key pressed: {pressed_key}")
                        
                        # Show immediate feedback on LCD when key is pressed
                        if lcd_controller:
                            current_display = f"{code}{pressed_key}"  # Show what code will be
                            if len(current_display) <= 10:  # "Code: " + digits fits on one line
                                lcd_controller.show_message("Code:", current_display)
                            else:
                                line1 = f"Code: {current_display[:11]}"
                                line2 = current_display[11:27]
                                lcd_controller.show_message(line1, line2)

                elif pressed_key is None and current_pressed_key:
                    # Key was released
                    print(f"DEBUG: Key '{current_pressed_key}' released")
                    print(f"Key released: {current_pressed_key}")
                    self.stop_key_tone()

                    # Add to code if key was pressed long enough (debounce)
                    if key_start_time and (current_time - key_start_time) > 0.1:
                        code += current_pressed_key
                        last_key_time = current_time
                        print(f"Code updated: {code}")
                        
                        # Update LCD display with entered digits
                        if lcd_controller:
                            if len(code) <= 16:  # Single line if fits
                                lcd_controller.show_message("Code:", code)
                            else:  # Split across two lines if too long
                                line1 = f"Code: {code[:11]}"  # "Code: " + 11 chars
                                line2 = code[11:27]  # Up to 16 more chars on line 2
                                lcd_controller.show_message(line1, line2)

                    current_pressed_key = None
                    key_start_time = None

                    # DO NOT restart idle tone after input has started
                    # The user is now in "input mode"

                time.sleep(0.005)  # Reduced delay for faster response (5ms instead of 20ms)

        finally:
            # Always clean up any ongoing tones when exiting
            if current_pressed_key:
                self.stop_key_tone()
            else:
                self.stop_any_tone()  # Stop any remaining tones

        return code if code else None
    
    def cleanup(self):
        """Clean up keypad resources"""
        # Stop any ongoing tones
        self.stop_any_tone()
        print("Keypad cleanup completed")
