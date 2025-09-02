#!/usr/bin/env python3
"""
Simple test for PyAudio installation and basic functionality
"""

def test_pyaudio_installation():
    """Test if PyAudio is installed and working"""
    print("Testing PyAudio installation...")
    
    try:
        import pyaudio
        print("✓ PyAudio imported successfully")
        
        # Test PyAudio initialization
        pa = pyaudio.PyAudio()
        print("✓ PyAudio initialized successfully")
        
        # Get device info
        device_count = pa.get_device_count()
        print(f"✓ Found {device_count} audio devices")
        
        # Get default device
        default_device = pa.get_default_output_device_info()
        print(f"✓ Default output device: {default_device['name']}")
        
        pa.terminate()
        print("✓ PyAudio terminated successfully")
        
        return True
        
    except ImportError as e:
        print(f"✗ PyAudio import failed: {e}")
        return False
    except Exception as e:
        print(f"✗ PyAudio test failed: {e}")
        return False

def test_tone_generator():
    """Test ToneGenerator with PyAudio"""
    print("\nTesting ToneGenerator with PyAudio...")
    
    try:
        from tones import ToneGenerator
        print("✓ ToneGenerator imported successfully")
        
        tones = ToneGenerator()
        print("✓ ToneGenerator initialized successfully")
        
        # Test simple tone generation (don't play it)
        tone_data = tones.generate_tone(440, 0.1)  # 100ms test tone
        print(f"✓ Generated tone data: {len(tone_data)} samples")
        
        # Test dual tone generation  
        dtmf_data = tones.generate_dual_tone(697, 1209, 0.1)  # DTMF "1"
        print(f"✓ Generated DTMF data: {len(dtmf_data)} samples")
        
        tones.cleanup()
        print("✓ ToneGenerator cleanup completed")
        
        return True
        
    except ImportError as e:
        print(f"✗ ToneGenerator import failed: {e}")
        return False
    except Exception as e:
        print(f"✗ ToneGenerator test failed: {e}")
        return False

def main():
    print("=== PyAudio Migration Test ===")
    
    # Test PyAudio installation
    pyaudio_ok = test_pyaudio_installation()
    
    # Test ToneGenerator
    tone_generator_ok = test_tone_generator()
    
    print("\n=== Test Results ===")
    print(f"PyAudio installation: {'PASS' if pyaudio_ok else 'FAIL'}")
    print(f"ToneGenerator:        {'PASS' if tone_generator_ok else 'FAIL'}")
    
    if pyaudio_ok and tone_generator_ok:
        print("\n✓ All tests passed! PyAudio migration is successful.")
    else:
        print("\n✗ Some tests failed. Please check the errors above.")

if __name__ == "__main__":
    main()
