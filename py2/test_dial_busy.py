#!/usr/bin/env python3
"""
Test script for dial tones and busy tones
Tests complex tone patterns and cadences
"""
import time
import sys
from tones import ToneGenerator
from countries import COUNTRIES

def test_dial_tone(country_code="7", duration=5):
    """Test country-specific dial tone"""
    print(f"Testing dial tone for country code {country_code}...")
    
    if country_code not in COUNTRIES:
        print(f"Country code {country_code} not found")
        return
        
    country = COUNTRIES[country_code]
    dial_params = country["dial_tone"]
    
    print(f"Country: {country['name']}")
    print(f"Dial tone type: {dial_params['type']}")
    print(f"Frequency: {dial_params['frequency']}")
    print(f"Cadence: {dial_params['cadence']}")
    
    tones = ToneGenerator()
    
    try:
        print(f"Playing dial tone for {duration} seconds...")
        tones.playing = True  # Set flag for interruption
        tones.generate_dial_tone(dial_params, duration=duration)
        print("Dial tone completed")
        
    except KeyboardInterrupt:
        print("\nDial tone interrupted by user")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        tones.playing = False
        tones.cleanup()

def test_busy_tone(country_code="7", duration=5):
    """Test country-specific busy tone"""
    print(f"Testing busy tone for country code {country_code}...")
    
    if country_code not in COUNTRIES:
        print(f"Country code {country_code} not found")
        return
        
    country = COUNTRIES[country_code]
    busy_params = country["busy_tone"]
    
    print(f"Country: {country['name']}")
    print(f"Busy tone type: {busy_params['type']}")
    print(f"Frequency: {busy_params['frequency']}")
    print(f"Cadence: {busy_params['cadence']}")
    
    tones = ToneGenerator()
    
    try:
        print(f"Playing busy tone for {duration} seconds...")
        tones.playing = True  # Set flag for interruption
        tones.generate_busy_tone(busy_params, duration=duration)
        print("Busy tone completed")
        
    except KeyboardInterrupt:
        print("\nBusy tone interrupted by user")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        tones.playing = False
        tones.cleanup()

def test_all_countries_dial():
    """Test dial tones for all countries"""
    print("Testing dial tones for all countries...")
    
    for code, country in COUNTRIES.items():
        print(f"\n{'='*50}")
        print(f"Testing {country['name']} (code: {code})")
        try:
            test_dial_tone(code, duration=3)
            time.sleep(1)  # Pause between tests
        except KeyboardInterrupt:
            print("\nTest interrupted by user")
            break

def test_all_countries_busy():
    """Test busy tones for all countries"""
    print("Testing busy tones for all countries...")
    
    for code, country in COUNTRIES.items():
        print(f"\n{'='*50}")
        print(f"Testing {country['name']} (code: {code})")
        try:
            test_busy_tone(code, duration=3)
            time.sleep(1)  # Pause between tests
        except KeyboardInterrupt:
            print("\nTest interrupted by user")
            break

def test_complex_patterns():
    """Test specific complex patterns"""
    print("Testing complex tone patterns...")
    
    # Test Australia's complex AM dial tone
    print("\n" + "="*50)
    print("Testing Australia's AM modulated dial tone...")
    test_dial_tone("61", duration=8)
    
    # Test Canada's dual frequency tones
    print("\n" + "="*50) 
    print("Testing Canada's dual frequency tones...")
    test_dial_tone("1", duration=5)
    time.sleep(1)
    test_busy_tone("1", duration=5)

def main():
    print("=== Dial & Busy Tone Test ===")
    
    if len(sys.argv) < 2:
        print("Usage: python3 test_dial_busy.py [dial|busy|all_dial|all_busy|complex] [country_code] [duration]")
        print("Available country codes:")
        for code, country in COUNTRIES.items():
            print(f"  {code}: {country['name']}")
        return
    
    test_type = sys.argv[1].lower()
    country_code = sys.argv[2] if len(sys.argv) > 2 else "7"
    duration = int(sys.argv[3]) if len(sys.argv) > 3 else 5
    
    try:
        if test_type == "dial":
            test_dial_tone(country_code, duration)
        elif test_type == "busy":
            test_busy_tone(country_code, duration)
        elif test_type == "all_dial":
            test_all_countries_dial()
        elif test_type == "all_busy":
            test_all_countries_busy()
        elif test_type == "complex":
            test_complex_patterns()
        else:
            print("Invalid test type. Use: dial, busy, all_dial, all_busy, or complex")
    except KeyboardInterrupt:
        print("\nTest interrupted by user")

if __name__ == "__main__":
    main()
