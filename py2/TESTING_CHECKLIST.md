# Checklist тестирования PyAudio миграции

## 🚀 Быстрые тесты

```bash
# 1. Проверка установки
python test_pyaudio_migration.py

# 2. Простые тоны
python test_simple_tones.py all

# 3. Диал и Busy тоны
python test_dial_busy.py complex
```

## 📋 Подробная проверка

### ✅ Базовые тоны
- [ ] `python test_simple_tones.py simple` - простой тон 440Hz
- [ ] `python test_simple_tones.py dtmf` - DTMF тон (клавиша "5")
- [ ] `python test_simple_tones.py continuous` - непрерывный тон
- [ ] `python test_simple_tones.py continuous_dtmf` - непрерывный DTMF

### ✅ Dial тоны (по странам)
- [ ] `python test_dial_busy.py dial 7 3` - Россия (одиночная частота)
- [ ] `python test_dial_busy.py dial 1 3` - Канада (двойная частота)  
- [ ] `python test_dial_busy.py dial 61 3` - Австралия (AM модуляция)
- [ ] `python test_dial_busy.py all_dial` - все страны

### ✅ Busy тоны (по странам)
- [ ] `python test_dial_busy.py busy 7 3` - Россия
- [ ] `python test_dial_busy.py busy 1 3` - Канада (двойная частота)
- [ ] `python test_dial_busy.py busy 61 3` - Австралия
- [ ] `python test_dial_busy.py all_busy` - все страны

### ✅ Сложные паттерны
- [ ] `python test_dial_busy.py complex` - AM модуляция + сложные каденции

## 🎵 Типы тонов, которые должны работать

### 1. Single frequency тоны
- Россия: 425Hz
- Австрия: 450Hz
- Япония: 400Hz

### 2. Dual frequency тоны  
- Канада dial: 440Hz + 480Hz
- Канада busy: 480Hz + 620Hz

### 3. AM modulated тоны
- Австралия: 425Hz carrier, 25Hz modulation
- Япония: 400Hz carrier, AM модуляция
- Индия: 400Hz carrier, AM модуляция

### 4. Сложные каденции
- Австралия dial: [0.4s on, 0.2s off, 0.4s on, 2.0s off]
- Сербия dial: [1.0s on, 9.0s off]
- Различные busy каденции от 0.2s до 0.6s

## 🐛 На что обратить внимание

- [ ] Нет ошибок импорта PyAudio
- [ ] Нет ошибок в threading (непрерывные тоны)
- [ ] Правильное освобождение ресурсов (cleanup)
- [ ] Чистый звук без артефактов
- [ ] Корректная работа start/stop методов

## ✅ Все тесты пройдены успешно!

Система готова к развертыванию на Raspberry Pi.
