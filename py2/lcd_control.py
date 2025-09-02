"""
LCD Display Controller for Looperphone
Controls 16x2 LCD display via I2C
"""
from RPLCD.i2c import CharLCD

class LCDController:
    def __init__(self, i2c_address=0x27):
        """Initialize LCD display"""
        try:
            self.lcd = CharLCD('PCF8574', i2c_address)
            self.lcd.clear()
            print("LCD initialized")
        except Exception as e:
            print(f"LCD initialization failed: {e}")
            self.lcd = None
    
    def show_message(self, line1="", line2=""):
        """Display message on LCD (16 chars per line)"""
        if not self.lcd:
            print(f"LCD: {line1} | {line2}")
            return
        
        try:
            self.lcd.clear()
            
            # Ensure lines don't exceed 16 characters
            line1 = line1[:16]
            line2 = line2[:16]
            
            self.lcd.cursor_pos = (0, 0)
            self.lcd.write_string(line1)
            
            if line2:
                self.lcd.cursor_pos = (1, 0)
                self.lcd.write_string(line2)
                
        except Exception as e:
            print(f"LCD error: {e}")
    
    def clear(self):
        """Clear LCD display"""
        if self.lcd:
            try:
                self.lcd.clear()
            except Exception as e:
                print(f"LCD clear error: {e}")
    
    def cleanup(self):
        """Clean up LCD resources"""
        if self.lcd:
            try:
                self.lcd.clear()
                self.lcd.close(clear=True)
            except Exception as e:
                print(f"LCD cleanup error: {e}")
