# Looperphone File Structure

## Core System Files

- **`main.py`** - Main application loop, manages call flow
- **`lcd_control.py`** - LCD display controller (16x2 I2C)
- **`keypad_control.py`** - Matrix keypad with DTMF tone generation
- **`tones.py`** - Dial tone and busy tone generator
- **`audio_player.py`** - MP3 file playback using mpg123
- **`countries.py`** - Country database with tone parameters

## Installation & Setup

- **`requirements.txt`** - Python package dependencies
- **`install.sh`** - System installation script (run as sudo)
- **`setup.sh`** - Quick setup for file permissions
- **`README.md`** - Complete documentation

## Testing & Diagnostics

- **`config.py`** - System diagnostics and configuration check
- **`simple_test.py`** - Individual component testing
- **`test_components.py`** - Comprehensive component tests
- **`run.py`** - Production launcher with logging

## Audio Files

- **`audio/`** - Directory for country MP3 files
- **`audio/README.txt`** - Audio file naming guide

## Quick Start

1. Copy all files to Raspberry Pi
2. Run: `sudo chmod +x setup.sh && ./setup.sh`
3. Install: `sudo ./install.sh`
4. Reboot: `sudo reboot`
5. Test: `python3 config.py test`
6. Run: `python3 run.py`

## Architecture Overview

```
main.py (Main Loop)
├── lcd_control.py (Display)
├── keypad_control.py (Input + DTMF)
├── tones.py (Dial/Busy Tones)  
├── audio_player.py (MP3 Playback)
└── countries.py (Configuration)
```

## Call Flow

1. **Idle**: "Pick up the phone"
2. **Pickup**: "Enter country code" + dial tone (440Hz)
3. **Input**: Code entry with DTMF feedback  
4. **Recognition**: Display country name
5. **Dialing**: Country-specific dial tone (10s)
6. **Announcement**: Play "{country}.mp3" if available
7. **Busy**: Country-specific busy tone (5s)
8. **Hangup**: Return to idle

System can be interrupted at any time by hanging up the phone.
