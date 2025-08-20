# numpad.py
import RPi.GPIO as GPIO
import time
import subprocess
import threading
import logging
from dtmf_frequencies import get_dtmf_frequency
from tone_player import TonePlayer

logger = logging.getLogger(__name__)


class Numpad:
    def __init__(self):
        # GPIO пины для матричной клавиатуры
        self.COLUMN_PINS = [17, 27, 22]  # столбцы
        self.ROW_PINS = [0, 5, 6, 13]  # строки

        self.NUMPAD_BUTTONS = [
            "1",
            "2",
            "3",
            "4",
            "5",
            "6",
            "7",
            "8",
            "9",
            "*",
            "0",
            "#",
        ]

        self.button_is_pressed = False
        self.current_button = None

        # Callback функции, которые будут установлены классом Phone
        self.on_button_press = None
        self.can_play_click_sound = None
        self.can_play_tone = None

        # Инициализация TonePlayer
        self.tone_player = TonePlayer()

        # Настройка GPIO
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)

        # Настройка пинов
        for pin in self.COLUMN_PINS:
            GPIO.setup(pin, GPIO.OUT)
            GPIO.output(pin, GPIO.HIGH)

        for pin in self.ROW_PINS:
            GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

        logger.info("Инициализация цифровой клавиатуры завершена")

        # Запуск потока для сканирования клавиатуры
        self.scanning = True
        self.scan_thread = threading.Thread(target=self._scan_keyboard, daemon=True)
        self.scan_thread.start()

    def _scan_keyboard(self):
        """Сканирует матричную клавиатуру в отдельном потоке"""
        while self.scanning:
            for col_index, col_pin in enumerate(self.COLUMN_PINS):
                # Активируем текущий столбец
                GPIO.output(col_pin, GPIO.LOW)

                # Проверяем все строки
                for row_index, row_pin in enumerate(self.ROW_PINS):
                    if GPIO.input(row_pin) == GPIO.LOW:
                        # Определяем нажатую кнопку
                        button_index = row_index * 3 + col_index
                        if button_index < len(self.NUMPAD_BUTTONS):
                            button_text = self.NUMPAD_BUTTONS[button_index]
                            self._handle_button_press(button_text)

                            # Ждем отпускания кнопки
                            while GPIO.input(row_pin) == GPIO.LOW:
                                time.sleep(0.01)

                            self._handle_button_release()

                # Деактивируем столбец
                GPIO.output(col_pin, GPIO.HIGH)

            time.sleep(0.01)  # Небольшая задержка для стабильности

    def _handle_button_press(self, button_text: str):
        """Обработка нажатия кнопки"""
        if self.current_button == button_text:
            return

        self.current_button = button_text
        logger.info(f"Физическая кнопка нажата: {button_text}")

        # Воспроизведение звука клика
        if self.can_play_click_sound and self.can_play_click_sound():
            self._play_click_sound()

        # Воспроизведение DTMF тона
        if self.can_play_tone and self.can_play_tone():
            frequencies = get_dtmf_frequency(button_text)
            self.tone_player.start(frequencies)

    def _handle_button_release(self):
        """Обработка отпускания кнопки"""
        if self.current_button:
            button_text = self.current_button

            # Останавливаем воспроизведение тона
            self.tone_player.stop_all()

            # Вызываем callback если он установлен
            if self.on_button_press:
                self.on_button_press(button_text)

            self.current_button = None
            logger.info(f"Кнопка отпущена: {button_text}")

    def _play_click_sound(self):
        """Воспроизведение звука клика"""
        try:
            # Предполагаем, что файл click.mp3 находится в assets папке
            # subprocess.Popen(["mpg123", "-q", "assets/click.mp3"])
            return True
        except Exception as e:
            logger.error(f"Ошибка воспроизведения звука клика: {e}")

    def get_numpad_buttons(self) -> list[str]:
        """Возвращает список кнопок клавиатуры"""
        return self.NUMPAD_BUTTONS.copy()

    def cleanup(self):
        """Очистка ресурсов"""
        self.scanning = False
        if self.scan_thread.is_alive():
            self.scan_thread.join()
        GPIO.cleanup()
        logger.info("Очистка ресурсов клавиатуры завершена")
