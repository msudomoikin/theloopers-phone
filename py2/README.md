# Looperphone - Raspberry Pi Payphone System

A complete payphone simulation system for Raspberry Pi with authentic dial and busy tones from different countries.

## Features

- **Hook Switch Detection**: Responds to phone pickup/hangup
- **Matrix Keypad**: 4x3 keypad with DTMF tone generation
- **LCD Display**: 16x2 character display for user feedback
- **Country-Specific Tones**: Authentic dial and busy tones for 9 countries
- **Audio Playback**: MP3 announcements for each country
- **Interrupt Handling**: Can be stopped at any time by hanging up

## Hardware Requirements

### Raspberry Pi 3B+ with:
- **LCD Display**: 16x2 I2C LCD (address 0x27)
  - SDA → GPIO2
  - SCL → GPIO3
- **Matrix Keypad**: 4x3 keypad
  - Columns → GPIO17, GPIO27, GPIO22
  - Rows → GPIO0, GPIO5, GPIO6, GPIO13
- **Hook Switch**: Phone handset switch
  - GPIO23 ↔ GND when picked up

## Software Dependencies

- Python 3.7+
- sounddevice (audio generation)
- numpy (signal processing)  
- RPLCD (LCD control)
- smbus2 (I2C communication)
- RPi.GPIO (GPIO control)
- mpg123 (MP3 playback)

## Installation

```bash
# Clone repository
git clone <repository-url>
cd theloopers-phone/py2

# Run installation script
sudo chmod +x install.sh
sudo ./install.sh

# Reboot system
sudo reboot
```

## Usage

```bash
# Run the application
python3 main.py

# Test I2C LCD connection
i2cdetect -y 1

# Enable autostart (optional)
sudo systemctl enable looperphone.service
```

## Call Flow

1. **Idle State**: Display shows "Pick up the phone"
2. **Phone Pickup**: Display shows "Enter country code", plays dial tone (440Hz)
3. **Code Entry**: User enters country code, each key plays DTMF tone
4. **Country Recognition**: Display shows country name
5. **Dialing**: Plays country-specific dial tone for 10 seconds
6. **Announcement**: Plays MP3 file "{country}.mp3" if available
7. **Busy Signal**: Plays country-specific busy tone for 5 seconds
8. **Hangup**: Returns to idle state

## Supported Countries

| Code | Country | Dial Tone | Busy Tone |
|------|---------|-----------|-----------|
| 7 | Russia | 425Hz | 425Hz |
| 1 | Canada | 440+480Hz | 480+620Hz |
| 61 | Australia | 425Hz AM | 425Hz |
| 81 | Japan | 400Hz AM | 400Hz |
| 91 | India | 400Hz AM | 400Hz |
| 43 | Austria | 450Hz | 450Hz |
| 381 | Serbia | 450Hz AM | 425Hz |
| 224 | Guinea | 450Hz | 450Hz |
| 92 | Pakistan | 400Hz | 425Hz |

## Audio Files

Place country MP3 files in the `audio/` directory:
- `russia.mp3`
- `canada.mp3`
- `australia.mp3`
- `japan.mp3`
- etc.

## Architecture

```
main.py              # Main loop and call flow control
├── lcd_control.py   # 16x2 LCD display management
├── keypad_control.py # Matrix keypad with DTMF tones
├── tones.py         # Dial/busy tone generation
├── audio_player.py  # MP3 file playback
└── countries.py     # Country database and tone parameters
```

## Configuration

Edit `countries.py` to add/modify country codes and their tone parameters.

## Troubleshooting

- **LCD not working**: Check I2C with `i2cdetect -y 1`, verify address 0x27
- **No audio**: Check audio output with `aplay /usr/share/sounds/alsa/Front_Left.wav`
- **Keypad issues**: Verify GPIO connections and pull-up resistors
- **Permission errors**: Add user to GPIO group: `sudo usermod -a -G gpio $USER`

## License

MIT License
