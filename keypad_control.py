#!/usr/bin/env python3
import RPi.GPIO as GPIO
import time
from tones import ToneGenerator

class KeypadControl:
    def __init__(self):
        """Инициализация клавиатуры"""
        # Настройка GPIO для клавиатуры
        GPIO.setmode(GPIO.BOARD)
        
        # Определение пинов
        self.rows = [33, 31, 29, 27]    # GPIO номера для строк
        self.cols = [15, 13, 11]        # GPIO номера для столбцов
        
        # Настройка строк как выходов
        for row in self.rows:
            GPIO.setup(row, GPIO.OUT)
            GPIO.output(row, GPIO.HIGH)
        
        # Настройка столбцов как входов с pull-up
        for col in self.cols:
            GPIO.setup(col, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        
        # Матрица клавиш
        self.keymap = [
            ['1', '2', '3'],
            ['4', '5', '6'],
            ['7', '8', '9'],
            ['*', '0', '#']
        ]
        
        # Генератор тонов для клавиш
        self.audio = ToneGenerator()
        
        print("Клавиатура инициализирована")
    
    def get_key(self):
        """Чтение нажатой клавиши"""
        key_pressed = None
        
        try:
            # Сканирование строк
            for row_idx, row_pin in enumerate(self.rows):
                GPIO.output(row_pin, GPIO.LOW)
                
                # Проверка столбцов
                for col_idx, col_pin in enumerate(self.cols):
                    if GPIO.input(col_pin) == GPIO.LOW:
                        key_pressed = self.keymap[row_idx][col_idx]
                        # Воспроизведение тона нажатия
                        self.audio.play_dtmf_tone(key_pressed)
                        break
                
                GPIO.output(row_pin, GPIO.HIGH)
                
                if key_pressed:
                    break
                    
        except Exception as e:
            print(f"Ошибка чтения клавиатуры: {e}")
        
        return key_pressed
    
    def get_code(self, timeout=3):
        """Получение кода страны с таймаутом"""
        code = ""
        last_key_time = time.time()
        
        print("Ожидание ввода кода...")
        
        while True:
            key = self.get_key()
            
            if key:
                code += key
                last_key_time = time.time()
                print(f"Текущий код: {code}")
            
            # Проверка таймаута
            if time.time() - last_key_time > timeout and code:
                break
            
            # Проверка максимальной длины (3 цифры)
            if len(code) >= 3:
                break
            
            time.sleep(0.1)
        
        return code if code else None