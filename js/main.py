#!/usr/bin/env python3
import RPi.GPIO as GPIO
import time
import threading
from enum import Enum
import signal
import sys

# Импорт модулей проекта
from lcd_control import LCDControl
from keypad_control import KeypadControl
from tones import ToneGenerator, CountryTones
from audio_player import AudioPlayer

# Конфигурация GPIO
HOOK_SWITCH_PIN = 23  # GPIO23 для определения состояния трубки

class PhoneState(Enum):
    IDLE = 0
    DIAL_TONE = 1
    ENTERING_CODE = 2
    DIALING = 3
    PLAYING_MESSAGE = 4
    BUSY_TONE = 5

class LooperPhone:
    def __init__(self):
        # Инициализация компонентов
        self.lcd = LCDControl()
        self.keypad = KeypadControl()
        self.audio = ToneGenerator()
        self.player = AudioPlayer()
        
        # Состояние системы
        self.state = PhoneState.IDLE
        self.running = True
        self.current_country = None
        self.dial_thread = None
        
        # Настройка GPIO
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(HOOK_SWITCH_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        
        # Обработка сигналов для корректного завершения
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)
    
    def signal_handler(self, sig, frame):
        """Обработка сигналов завершения"""
        print("Завершение работы...")
        self.running = False
        self.cleanup()
        sys.exit(0)
    
    def check_hook_switch(self):
        """Проверка состояния трубки"""
        return GPIO.input(HOOK_SWITCH_PIN) == GPIO.LOW
    
    def run(self):
        """Главный цикл программы"""
        print("LooperPhone запущен")
        
        try:
            while self.running:
                if self.check_hook_switch():
                    # Трубка поднята
                    if self.state == PhoneState.IDLE:
                        self.handle_phone_picked_up()
                    
                    # Обработка текущего состояния
                    if self.state == PhoneState.DIAL_TONE:
                        time.sleep(0.1)
                    
                    elif self.state == PhoneState.ENTERING_CODE:
                        self.handle_code_entry()
                    
                    elif self.state == PhoneState.DIALING:
                        time.sleep(0.1)
                    
                    elif self.state == PhoneState.PLAYING_MESSAGE:
                        time.sleep(0.1)
                    
                    elif self.state == PhoneState.BUSY_TONE:
                        time.sleep(0.1)
                
                else:
                    # Трубка положена
                    if self.state != PhoneState.IDLE:
                        self.handle_phone_hung_up()
                    
                    self.state = PhoneState.IDLE
                    self.lcd.show_message("Pick up the phone", "")
                    time.sleep(0.5)
        
        except Exception as e:
            print(f"Ошибка в главном цикле: {e}")
            self.cleanup()
    
    def handle_phone_picked_up(self):
        """Обработка поднятия трубки"""
        print("Трубка поднята")
        self.state = PhoneState.DIAL_TONE
        self.lcd.show_message("Enter country", "code")
        
        # Запуск стандартного гудка
        self.audio.play_russia_dial_tone(loop=True)
    
    def handle_code_entry(self):
        """Обработка ввода кода страны"""
        print("Ожидание ввода кода страны...")
        country_code = self.keypad.get_code(timeout=3)
        
        if country_code:
            print(f"Набран код: {country_code}")
            self.lcd.show_message("Code entered:", country_code)
            
            # Проверка существования страны
            if country_code in CountryTones.DIAL_TONES:
                self.current_country = country_code
                self.state = PhoneState.DIALING
                self.start_dialing()
            else:
                self.lcd.show_message("Unknown", "country")
                time.sleep(2)
                self.state = PhoneState.DIAL_TONE
                self.audio.play_russia_dial_tone(loop=True)
    
    def start_dialing(self):
        """Запуск процесса дозвона"""
        # Остановка предыдущего тона
        self.audio.stop()
        
        # Отображение названия страны
        country_name = CountryTones.COUNTRY_NAMES.get(self.current_country, "Unknown")
        self.lcd.show_message("Dialing:", country_name)
        
        # Запуск соответствующего dial tone
        self.dial_thread = threading.Thread(target=self.play_dial_tone_and_wait)
        self.dial_thread.daemon = True
        self.dial_thread.start()
    
    def play_dial_tone_and_wait(self):
        """Воспроизведение dial tone и ожидание"""
        # Воспроизведение dial tone в течение 10 секунд
        self.audio.play_country_dial_tone(self.current_country, duration=10)
        
        # Проверка, не положили ли трубку
        if self.state == PhoneState.DIALING:
            # Проигрывание MP3 файла
            self.state = PhoneState.PLAYING_MESSAGE
            self.player.play_country_message(self.current_country)
            
            # Проверка, не положили ли трубку во время проигрывания
            if self.state == PhoneState.PLAYING_MESSAGE:
                # Воспроизведение busy tone
                self.state = PhoneState.BUSY_TONE
                self.play_busy_tone()
    
    def play_busy_tone(self):
        """Воспроизведение busy tone"""
        self.audio.play_country_busy_tone(self.current_country, duration=5)
        
        # После busy tone сброс состояния
        if self.state == PhoneState.BUSY_TONE:
            self.state = PhoneState.DIAL_TONE
            self.audio.play_russia_dial_tone(loop=True)
            self.lcd.show_message("Enter country", "code")
    
    def handle_phone_hung_up(self):
        """Обработка положения трубки"""
        print("Трубка положена")
        
        # Остановка всех процессов
        self.audio.stop()
        self.player.stop()
        
        # Сброс состояния
        self.state = PhoneState.IDLE
        self.current_country = None
        
        # Очистка дисплея
        self.lcd.clear()
    
    def cleanup(self):
        """Очистка ресурсов"""
        print("Очистка ресурсов...")
        self.audio.stop()
        self.player.stop()
        self.lcd.clear()
        GPIO.cleanup()

if __name__ == "__main__":
    phone = LooperPhone()
    phone.run()