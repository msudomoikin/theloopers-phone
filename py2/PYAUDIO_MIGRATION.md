# PyAudio Migration Documentation

## Overview
Генерация тонов в проекте theloopers-phone была переписана с использования sounddevice на PyAudio для улучшения производительности и совместимости.

## Changes Made

### 1. Updated Dependencies
- **requirements.txt**: Заменил `sounddevice>=0.4.1` на `pyaudio>=0.2.11`

### 2. Rewritten ToneGenerator Class (`tones.py`)
- Полностью переписан класс `ToneGenerator` для использования PyAudio
- Добавлена поддержка потоков (threading) для непрерывного воспроизведения
- Улучшена обработка ошибок
- Добавлены методы для управления PyAudio потоками

#### Key Changes:
- `__init__()`: Инициализация PyAudio вместо sounddevice
- `_play_tone_data()`: Новый внутренний метод для воспроизведения данных через PyAudio
- `start_continuous_tone()`: Использует threading для непрерывного воспроизведения
- `play_dtmf_tone_continuous()`: Переписан с использованием PyAudio потоков
- `cleanup()`: Правильное освобождение ресурсов PyAudio

### 3. Updated KeypadController (`keypad_control.py`)
- Удален прямой импорт sounddevice
- Удален импорт numpy (не используется напрямую)
- Все методы теперь используют ToneGenerator вместо прямого sounddevice
- Улучшена обработка отсутствующего tone_generator

#### Key Changes:
- `start_idle_tone()`: Использует `ToneGenerator.start_continuous_tone()`
- `start_key_tone()`: Использует `ToneGenerator.play_dtmf_tone_continuous()`
- `stop_key_tone()`: Использует `ToneGenerator.stop_dtmf_tone()`
- `stop_any_tone()`: Использует `ToneGenerator.stop_continuous_tone()`

## Benefits of PyAudio Migration

1. **Better Performance**: PyAudio предоставляет более низкоуровневый контроль над аудио потоками
2. **Threading Support**: Улучшенная поддержка многопоточности для непрерывного воспроизведения
3. **Resource Management**: Лучшее управление аудио ресурсами
4. **Compatibility**: Более стабильная работа на различных системах

## Installation

Для установки PyAudio на Raspberry Pi:

```bash
# Update system
sudo apt-get update

# Install system dependencies
sudo apt-get install portaudio19-dev python3-pyaudio

# Install Python package
pip install pyaudio>=0.2.11
```

## Testing

Используйте новый тестовый скрипт для проверки:

```bash
python3 test_pyaudio_migration.py
```

Этот скрипт проверит:
- Установку PyAudio
- Инициализацию ToneGenerator
- Генерацию тонов

## Compatibility

Все публичные методы ToneGenerator остались совместимыми:
- `start_continuous_tone(frequency, amplitude)`
- `stop_continuous_tone()`
- `play_dtmf_tone_continuous(freq1, freq2, amplitude)`
- `stop_dtmf_tone()`
- `generate_dial_tone(params, duration)`
- `generate_busy_tone(params, duration)`
- `cleanup()`

## Notes

- PyAudio может потребовать системных зависимостей (portaudio)
- На Raspberry Pi рекомендуется установка через apt-get для лучшей совместимости
- Все существующие скрипты должны работать без изменений
