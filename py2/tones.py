"""
Tone Generator for Looperphone
Generates dial tones and busy tones for different countries using PyAudio
"""

import time
import pyaudio
import numpy as np
import threading


class ToneGenerator:
    def __init__(self, sample_rate=44100):
        """Initialize tone generator with PyAudio"""
        self.sample_rate = sample_rate
        self.chunk_size = 1024
        self.format = pyaudio.paFloat32
        self.channels = 1
        
        # Initialize PyAudio
        self.pa = pyaudio.PyAudio()
        self.stream = None
        self.playing = False
        self.play_thread = None
        
        print("PyAudio tone generator initialized")

    def generate_tone(self, frequency, duration, amplitude=0.3):
        """Generate a simple sine wave tone"""
        t = np.linspace(0, duration, int(self.sample_rate * duration), False)
        tone = np.sin(2 * np.pi * frequency * t) * amplitude
        return tone.astype(np.float32)

    def generate_dual_tone(self, freq1, freq2, duration, amplitude=0.3):
        """Generate tone with two frequencies (DTMF)"""
        t = np.linspace(0, duration, int(self.sample_rate * duration), False)
        tone1 = np.sin(2 * np.pi * freq1 * t) * amplitude
        tone2 = np.sin(2 * np.pi * freq2 * t) * amplitude
        return ((tone1 + tone2) / 2).astype(np.float32)

    def generate_am_modulated_tone(
        self, carrier_freq, mod_freq, duration, mod_index=0.95, amplitude=0.3
    ):
        """Generate amplitude modulated tone"""
        t = np.linspace(0, duration, int(self.sample_rate * duration), False)
        carrier = np.sin(2 * np.pi * carrier_freq * t)
        modulator = np.sin(2 * np.pi * mod_freq * t)
        am_signal = carrier * (1 + mod_index * modulator) * amplitude
        return am_signal.astype(np.float32)

    def _play_tone_data(self, tone_data):
        """Play tone data using PyAudio stream"""
        try:
            if self.stream is None or not self.stream.is_active():
                self.stream = self.pa.open(
                    format=self.format,
                    channels=self.channels,
                    rate=self.sample_rate,
                    output=True,
                    frames_per_buffer=self.chunk_size
                )
            
            # Write tone data to stream in chunks
            for i in range(0, len(tone_data), self.chunk_size):
                if not self.playing:
                    break
                chunk = tone_data[i:i + self.chunk_size]
                self.stream.write(chunk.tobytes())
                
        except Exception as e:
            print(f"Play tone error: {e}")

    def play_tone(self, frequency, duration, amplitude=0.3):
        """Play a single tone"""
        try:
            tone = self.generate_tone(frequency, duration, amplitude)
            self.playing = True
            self._play_tone_data(tone)
            self.playing = False
        except Exception as e:
            print(f"Tone playback error: {e}")

    def start_continuous_tone(self, frequency, amplitude=0.3):
        """Start continuous tone in a separate thread"""
        try:
            self.stop_continuous_tone()  # Stop any existing tone
            
            def continuous_play():
                self.playing = True
                # Generate a short tone segment to loop
                duration = 0.5  # 500ms segments
                tone = self.generate_tone(frequency, duration, amplitude)
                
                if self.stream is None or not self.stream.is_active():
                    self.stream = self.pa.open(
                        format=self.format,
                        channels=self.channels,
                        rate=self.sample_rate,
                        output=True,
                        frames_per_buffer=self.chunk_size
                    )
                
                while self.playing:
                    try:
                        for i in range(0, len(tone), self.chunk_size):
                            if not self.playing:
                                break
                            chunk = tone[i:i + self.chunk_size]
                            self.stream.write(chunk.tobytes())
                    except Exception as e:
                        print(f"Continuous tone error: {e}")
                        break
            
            self.play_thread = threading.Thread(target=continuous_play)
            self.play_thread.daemon = True
            self.play_thread.start()
            
        except Exception as e:
            print(f"Start continuous tone error: {e}")

    def stop_continuous_tone(self):
        """Stop any currently playing tone"""
        try:
            self.playing = False
            if self.play_thread and self.play_thread.is_alive():
                self.play_thread.join(timeout=1.0)
            if self.stream and self.stream.is_active():
                self.stream.stop_stream()
        except Exception as e:
            print(f"Stop continuous tone error: {e}")

    def play_dtmf_tone_continuous(self, freq1, freq2, amplitude=0.3):
        """Start continuous DTMF tone in a separate thread"""
        try:
            self.stop_continuous_tone()  # Stop any existing tone
            
            def continuous_dtmf_play():
                self.playing = True
                # Generate a short DTMF tone segment to loop
                duration = 0.5  # 500ms segments
                tone = self.generate_dual_tone(freq1, freq2, duration, amplitude)
                
                if self.stream is None or not self.stream.is_active():
                    self.stream = self.pa.open(
                        format=self.format,
                        channels=self.channels,
                        rate=self.sample_rate,
                        output=True,
                        frames_per_buffer=self.chunk_size
                    )
                
                while self.playing:
                    try:
                        for i in range(0, len(tone), self.chunk_size):
                            if not self.playing:
                                break
                            chunk = tone[i:i + self.chunk_size]
                            self.stream.write(chunk.tobytes())
                    except Exception as e:
                        print(f"Continuous DTMF tone error: {e}")
                        break
            
            self.play_thread = threading.Thread(target=continuous_dtmf_play)
            self.play_thread.daemon = True
            self.play_thread.start()
            
        except Exception as e:
            print(f"DTMF tone error: {e}")

    def stop_dtmf_tone(self):
        """Stop DTMF tone"""
        self.stop_continuous_tone()

    def generate_dial_tone(self, params, duration=10):
        """Generate country-specific dial tone (can be interrupted)"""
        try:
            tone_type = params.get("type", "single")
            cadence = params.get("cadence", [1.0, 1.0])  # [on_time, off_time]

            start_time = time.time()
            cadence_index = 0

            while time.time() - start_time < duration:
                if not self.playing:
                    break
                    
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

                        # Play tone using PyAudio
                        self._play_tone_data(tone)

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

                    # Play tone using PyAudio
                    self._play_tone_data(tone)

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
                if not self.playing:
                    break
                    
                # Generate tone based on type
                if tone_type == "single":
                    frequency = params["frequency"]
                    tone = self.generate_tone(frequency, cadence[0])

                elif tone_type == "dual":
                    freq1, freq2 = params["frequency"]
                    tone = self.generate_dual_tone(freq1, freq2, cadence[0])

                # Play tone using PyAudio
                self._play_tone_data(tone)

                # Pause between tones
                time.sleep(cadence[1])

        except Exception as e:
            print(f"Busy tone error: {e}")

    def cleanup(self):
        """Clean up tone generator resources"""
        try:
            self.stop_continuous_tone()
            if self.stream:
                self.stream.close()
            self.pa.terminate()
            print("PyAudio tone generator cleanup completed")
        except Exception as e:
            print(f"Cleanup error: {e}")
