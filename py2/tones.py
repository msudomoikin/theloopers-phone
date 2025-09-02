"""
Tone Generator for Looperphone
Generates dial tones and busy tones for different countries
"""
import time
import threading
import sounddevice as sd
import numpy as np

class ToneGenerator:
    def __init__(self, sample_rate=44100):
        """Initialize tone generator"""
        self.sample_rate = sample_rate
        self.continuous_thread = None
        self.stop_continuous = False
        print("Tone generator initialized")
    
    def generate_tone(self, frequency, duration, amplitude=0.3):
        """Generate a simple sine wave tone"""
        t = np.linspace(0, duration, int(self.sample_rate * duration))
        tone = np.sin(2 * np.pi * frequency * t) * amplitude
        return tone
    
    def generate_dual_tone(self, freq1, freq2, duration, amplitude=0.3):
        """Generate tone with two frequencies"""
        t = np.linspace(0, duration, int(self.sample_rate * duration))
        tone1 = np.sin(2 * np.pi * freq1 * t) * amplitude
        tone2 = np.sin(2 * np.pi * freq2 * t) * amplitude
        return (tone1 + tone2) / 2
    
    def generate_am_modulated_tone(self, carrier_freq, mod_freq, duration, mod_index=0.95, amplitude=0.3):
        """Generate amplitude modulated tone"""
        t = np.linspace(0, duration, int(self.sample_rate * duration))
        carrier = np.sin(2 * np.pi * carrier_freq * t)
        modulator = np.sin(2 * np.pi * mod_freq * t)
        am_signal = carrier * (1 + mod_index * modulator) * amplitude
        return am_signal
    
    def start_continuous_tone(self, frequency, amplitude=0.3):
        """Start continuous tone (for dial tone while waiting)"""
        self.stop_continuous = False
        
        def play_continuous():
            while not self.stop_continuous:
                try:
                    tone = self.generate_tone(frequency, 0.1, amplitude)
                    sd.play(tone, self.sample_rate)
                    # time.sleep(0.05)
                except Exception as e:
                    print(f"Continuous tone error: {e}")
                    break
        
        self.continuous_thread = threading.Thread(target=play_continuous)
        self.continuous_thread.daemon = True
        self.continuous_thread.start()
    
    def stop_continuous_tone(self):
        """Stop continuous tone"""
        self.stop_continuous = True
        if self.continuous_thread:
            self.continuous_thread.join(timeout=1)
        sd.stop()
    
    def generate_dial_tone(self, params, duration=10):
        """Generate country-specific dial tone"""
        try:
            tone_type = params.get('type', 'single')
            cadence = params.get('cadence', [1.0, 1.0])  # [on_time, off_time]
            
            start_time = time.time()
            cadence_index = 0
            
            while time.time() - start_time < duration:
                # Handle complex cadence patterns (e.g., Australia: on-off-on-off)
                if cadence_index < len(cadence):
                    if cadence_index % 2 == 0:  # Even indices = tone on
                        tone_duration = cadence[cadence_index]
                        
                        # Generate tone based on type
                        if tone_type == 'single':
                            frequency = params['frequency']
                            tone = self.generate_tone(frequency, tone_duration)
                            
                        elif tone_type == 'dual':
                            freq1, freq2 = params['frequency']
                            tone = self.generate_dual_tone(freq1, freq2, tone_duration)
                            
                        elif tone_type == 'am':
                            carrier_freq = params['frequency']
                            mod_freq = params['mod_frequency']
                            mod_index = params.get('mod_index', 0.95)
                            tone = self.generate_am_modulated_tone(carrier_freq, mod_freq, tone_duration, mod_index)
                        
                        # Play tone
                        sd.play(tone, self.sample_rate)
                        sd.wait()  # Wait for tone to finish
                        
                    else:  # Odd indices = silence
                        silence_duration = cadence[cadence_index]
                        time.sleep(silence_duration)
                    
                    cadence_index += 1
                    
                    # Reset cadence for looping
                    if cadence_index >= len(cadence):
                        cadence_index = 0
                else:
                    # Simple two-element cadence [on, off]
                    if tone_type == 'single':
                        frequency = params['frequency']
                        tone = self.generate_tone(frequency, cadence[0])
                        
                    elif tone_type == 'dual':
                        freq1, freq2 = params['frequency']
                        tone = self.generate_dual_tone(freq1, freq2, cadence[0])
                        
                    elif tone_type == 'am':
                        carrier_freq = params['frequency']
                        mod_freq = params['mod_frequency']
                        mod_index = params.get('mod_index', 0.95)
                        tone = self.generate_am_modulated_tone(carrier_freq, mod_freq, cadence[0], mod_index)
                    
                    # Play tone
                    sd.play(tone, self.sample_rate)
                    sd.wait()  # Wait for tone to finish
                    
                    # Pause between tones
                    if len(cadence) > 1:
                        time.sleep(cadence[1])
                    
        except Exception as e:
            print(f"Dial tone error: {e}")
    
    def generate_busy_tone(self, params, duration=5):
        """Generate country-specific busy tone"""
        try:
            tone_type = params.get('type', 'single')
            cadence = params.get('cadence', [0.4, 0.4])  # [on_time, off_time]
            
            start_time = time.time()
            
            while time.time() - start_time < duration:
                # Generate tone based on type
                if tone_type == 'single':
                    frequency = params['frequency']
                    tone = self.generate_tone(frequency, cadence[0])
                    
                elif tone_type == 'dual':
                    freq1, freq2 = params['frequency']
                    tone = self.generate_dual_tone(freq1, freq2, cadence[0])
                
                # Play tone
                sd.play(tone, self.sample_rate)
                sd.wait()  # Wait for tone to finish
                
                # Pause between tones
                time.sleep(cadence[1])
                
        except Exception as e:
            print(f"Busy tone error: {e}")
    
    def cleanup(self):
        """Clean up tone generator resources"""
        self.stop_continuous_tone()
        print("Tone generator cleanup completed")
