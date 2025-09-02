#!/usr/bin/env python3
"""
Simple test for ToneGenerator without GPIO dependencies
Tests PyAudio-based tone generation
"""
import time
import sys
from tones import ToneGenerator

def test_simple_tone():
    """Test simple tone generation"""
    print("Testing simple tone generation...")
    tones = ToneGenerator()
    
    try:
        print("Playing 440Hz tone for 2 seconds...")
        tones.play_tone(440, 2.0, amplitude=0.3)
        print("Tone completed")
        
    except Exception as e:
        print(f"Error: {e}")
    finally:
        tones.cleanup()

def test_dtmf_tone():
    """Test DTMF tone generation"""
    print("Testing DTMF tone generation...")
    tones = ToneGenerator()
    
    try:
        # Test DTMF tone for key "5" (770Hz, 1336Hz)
        print("Playing DTMF tone for key '5' (770Hz + 1336Hz) for 1 second...")
        tone_data = tones.generate_dual_tone(770, 1336, 1.0, amplitude=0.3)
        tones._play_tone_data(tone_data)
        print("DTMF tone completed")
        
    except Exception as e:
        print(f"Error: {e}")
    finally:
        tones.cleanup()

def test_continuous_tone():
    """Test continuous tone with manual stop"""
    print("Testing continuous tone...")
    tones = ToneGenerator()
    
    try:
        print("Starting continuous 440Hz tone...")
        tones.start_continuous_tone(440, amplitude=0.3)
        print("Tone is playing... will stop in 3 seconds")
        
        time.sleep(3)
        
        print("Stopping continuous tone...")
        tones.stop_continuous_tone()
        print("Continuous tone stopped")
        
    except Exception as e:
        print(f"Error: {e}")
    finally:
        tones.cleanup()

def test_continuous_dtmf():
    """Test continuous DTMF tone"""
    print("Testing continuous DTMF tone...")
    tones = ToneGenerator()
    
    try:
        print("Starting continuous DTMF tone (697Hz + 1209Hz - key '1')...")
        tones.play_dtmf_tone_continuous(697, 1209, amplitude=0.3)
        print("DTMF tone is playing... will stop in 2 seconds")
        
        time.sleep(2)
        
        print("Stopping DTMF tone...")
        tones.stop_dtmf_tone()
        print("DTMF tone stopped")
        
    except Exception as e:
        print(f"Error: {e}")
    finally:
        tones.cleanup()

def main():
    print("=== PyAudio ToneGenerator Test ===")
    
    if len(sys.argv) < 2:
        print("Usage: python3 test_simple_tones.py [simple|dtmf|continuous|continuous_dtmf|all]")
        return
    
    test_type = sys.argv[1].lower()
    
    if test_type == "simple":
        test_simple_tone()
    elif test_type == "dtmf":
        test_dtmf_tone()
    elif test_type == "continuous":
        test_continuous_tone()
    elif test_type == "continuous_dtmf":
        test_continuous_dtmf()
    elif test_type == "all":
        test_simple_tone()
        print("\n" + "="*50 + "\n")
        test_dtmf_tone()
        print("\n" + "="*50 + "\n")
        test_continuous_tone()
        print("\n" + "="*50 + "\n")
        test_continuous_dtmf()
    else:
        print("Invalid test type. Use: simple, dtmf, continuous, continuous_dtmf, or all")

if __name__ == "__main__":
    main()
