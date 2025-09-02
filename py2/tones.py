"""
Tone Generator for Looperphone
Generates dial tones and busy tones for different countries
"""

import time
import sounddevice as sd
import numpy as np


class ToneGenerator:
    def __init__(self, sample_rate=44100):
        """Initialize tone generator"""
        self.sample_rate = sample_rate
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

    def generate_am_modulated_tone(
        self, carrier_freq, mod_freq, duration, mod_index=0.95, amplitude=0.3
    ):
        """Generate amplitude modulated tone"""
        t = np.linspace(0, duration, int(self.sample_rate * duration))
        carrier = np.sin(2 * np.pi * carrier_freq * t)
        modulator = np.sin(2 * np.pi * mod_freq * t)
        am_signal = carrier * (1 + mod_index * modulator) * amplitude
        return am_signal

    def start_continuous_tone(self, frequency, amplitude=0.3):
        """Start continuous tone (can be stopped with sd.stop())"""
        try:
            # Generate shorter buffer for faster start
            duration = 5.0  # Shorter buffer for faster generation
            tone = self.generate_tone(frequency, duration, amplitude)
            # Use non-blocking play for immediate start with loop
            sd.play(tone, self.sample_rate, blocking=False, loop=True)
        except Exception as e:
            print(f"Continuous tone error: {e}")

    def stop_continuous_tone(self):
        """Stop any currently playing tone"""
        try:
            sd.stop()
        except Exception as e:
            print(f"Stop continuous tone error: {e}")

    def play_dtmf_tone_continuous(self, freq1, freq2, amplitude=0.3):
        """Start continuous DTMF tone (can be stopped with sd.stop())"""
        try:
            # Generate shorter buffer for faster start
            duration = 5.0  # Shorter buffer for faster generation
            tone = self.generate_dual_tone(freq1, freq2, duration, amplitude)
            # Use non-blocking play for immediate start
            sd.play(tone, self.sample_rate, blocking=False)
        except Exception as e:
            print(f"DTMF tone error: {e}")

    def stop_dtmf_tone(self):
        """Stop DTMF tone"""
        try:
            sd.stop()
        except Exception as e:
            print(f"Stop DTMF tone error: {e}")

    def generate_dial_tone(self, params, duration=10):
        """Generate country-specific dial tone (can be interrupted)"""
        try:
            tone_type = params.get("type", "single")
            cadence = params.get("cadence", [1.0, 1.0])  # [on_time, off_time]

            start_time = time.time()
            cadence_index = 0

            while time.time() - start_time < duration:
                # Handle complex cadence patterns (e.g., Australia: on-off-on-off)
                if cadence_index < len(cadence):
                    if cadence_index % 2 == 0:  # Even indices = tone on
                        tone_duration = min(
                            cadence[cadence_index],
                            duration - (time.time() - start_time),
                        )
                        if tone_duration <= 0:
                            break

                        # Generate tone based on type
                        if tone_type == "single":
                            frequency = params["frequency"]
                            tone = self.generate_tone(frequency, tone_duration)

                        elif tone_type == "dual":
                            freq1, freq2 = params["frequency"]
                            tone = self.generate_dual_tone(freq1, freq2, tone_duration)

                        elif tone_type == "am":
                            carrier_freq = params["frequency"]
                            mod_freq = params["mod_frequency"]
                            mod_index = params.get("mod_index", 0.95)
                            tone = self.generate_am_modulated_tone(
                                carrier_freq, mod_freq, tone_duration, mod_index
                            )

                        # Play tone (non-blocking so it can be interrupted)
                        sd.play(tone, self.sample_rate)
                        sd.wait()  # Wait for tone to finish or be interrupted

                    else:  # Odd indices = silence
                        silence_duration = min(
                            cadence[cadence_index],
                            duration - (time.time() - start_time),
                        )
                        if silence_duration <= 0:
                            break
                        time.sleep(silence_duration)

                    cadence_index += 1

                    # Reset cadence for looping
                    if cadence_index >= len(cadence):
                        cadence_index = 0
                else:
                    # Simple two-element cadence [on, off]
                    remaining_time = duration - (time.time() - start_time)
                    tone_duration = min(cadence[0], remaining_time)

                    if tone_duration <= 0:
                        break

                    if tone_type == "single":
                        frequency = params["frequency"]
                        tone = self.generate_tone(frequency, tone_duration)

                    elif tone_type == "dual":
                        freq1, freq2 = params["frequency"]
                        tone = self.generate_dual_tone(freq1, freq2, tone_duration)

                    elif tone_type == "am":
                        carrier_freq = params["frequency"]
                        mod_freq = params["mod_frequency"]
                        mod_index = params.get("mod_index", 0.95)
                        tone = self.generate_am_modulated_tone(
                            carrier_freq, mod_freq, tone_duration, mod_index
                        )

                    # Play tone (non-blocking so it can be interrupted)
                    sd.play(tone, self.sample_rate)
                    sd.wait()  # Wait for tone to finish or be interrupted

                    # Pause between tones
                    if len(cadence) > 1:
                        remaining_time = duration - (time.time() - start_time)
                        pause_duration = min(cadence[1], remaining_time)
                        if pause_duration > 0:
                            time.sleep(pause_duration)

        except Exception as e:
            print(f"Dial tone error: {e}")

    def generate_busy_tone(self, params, duration=5):
        """Generate country-specific busy tone"""
        try:
            tone_type = params.get("type", "single")
            cadence = params.get("cadence", [0.4, 0.4])  # [on_time, off_time]

            start_time = time.time()

            while time.time() - start_time < duration:
                # Generate tone based on type
                if tone_type == "single":
                    frequency = params["frequency"]
                    tone = self.generate_tone(frequency, cadence[0])

                elif tone_type == "dual":
                    freq1, freq2 = params["frequency"]
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
        sd.stop()
        print("Tone generator cleanup completed")
