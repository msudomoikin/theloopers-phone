"""
Audio Player for Looperphone  
Plays MP3 files using mpg123 for country announcements
"""
import os
import subprocess

class AudioPlayer:
    def __init__(self, audio_dir="audio"):
        """Initialize audio player"""
        self.audio_dir = audio_dir
        self.current_process = None
        print("Audio player initialized")
    
    def play_country_file(self, country_name):
        """Play country MP3 file if it exists"""
        filename = f"{country_name}.mp3"
        filepath = os.path.join(self.audio_dir, filename)
        
        if os.path.exists(filepath):
            try:
                print(f"Playing: {filepath}")
                
                # Use mpg123 to play MP3 file
                self.current_process = subprocess.Popen(
                    ['mpg123', '-q', filepath],  # -q for quiet mode
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL
                )
                
                # Wait for playback to complete
                self.current_process.wait()
                
            except FileNotFoundError:
                print("mpg123 not found. Install with: sudo apt-get install mpg123")
            except Exception as e:
                print(f"Error playing {filepath}: {e}")
        else:
            print(f"Audio file not found: {filepath}")
    
    def stop_playback(self):
        """Stop current audio playback"""
        if self.current_process and self.current_process.poll() is None:
            try:
                self.current_process.terminate()
                self.current_process.wait(timeout=2)
            except subprocess.TimeoutExpired:
                self.current_process.kill()
            except Exception as e:
                print(f"Error stopping playback: {e}")
    
    def cleanup(self):
        """Clean up audio player resources"""
        self.stop_playback()
        print("Audio player cleanup completed")
