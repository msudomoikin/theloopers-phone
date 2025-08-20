# phone.py
import RPi.GPIO as GPIO
import time
import logging
from enum import Enum
from typing import Optional
from tone_player import tone_player_vanilla as tone_player
from numpad import Numpad
from utils import find_ringing_tone

logger = logging.getLogger(__name__)


class PhoneState(Enum):
    HANG = "hang"
    IDLE = "idle"
    DIALING = "dialing"
    CALL = "call"


class Phone:
    def __init__(self):
        # GPIO пины для кнопок управления
        self.PICK_BUTTON_PIN = 23  # Кнопка "поднять трубку"
        self.HANG_BUTTON_PIN = 24  # Кнопка "повесить трубку"
        self.CALL_BUTTON_PIN = 25  # Кнопка "вызов"

        # Инициализация состояния
        self._state = PhoneState.HANG
        self._screen_content = ""

        # Инициализация компонентов
        self.numpad = Numpad()
        self.setup_numpad_callbacks()

        # Настройка GPIO для кнопок
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)

        # Настройка кнопок с подтяжкой
        GPIO.setup(self.PICK_BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self.HANG_BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self.CALL_BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

        # Инициализация обработчиков кнопок
        self.initialize_control_buttons()

        logger.info("Инициализация телефона завершена")

    def setup_numpad_callbacks(self):
        """Настраивает обратные вызовы для цифровой клавиатуры"""

        # Установка callback для нажатия кнопок
        def on_button_press(button_text: str):
            if self._state == PhoneState.IDLE:
                self.screen = button_text
                logger.info(f"Добавлена цифра на экран: {button_text}")

        self.numpad.on_button_press = on_button_press

        # Установка callback для определения возможности воспроизведения звука клика
        def can_play_click_sound() -> bool:
            return self._state == PhoneState.HANG

        self.numpad.can_play_click_sound = can_play_click_sound

        # Установка callback для определения возможности воспроизведения тона
        def can_play_tone() -> bool:
            return self._state == PhoneState.IDLE

        self.numpad.can_play_tone = can_play_tone

    def initialize_control_buttons(self):
        """Инициализирует обработчики кнопок управления"""
        # Запуск потоков для отслеживания нажатий кнопок
        import threading

        # Поток для кнопки "поднять трубку"
        pick_thread = threading.Thread(target=self._monitor_pick_button, daemon=True)
        pick_thread.start()

        # Поток для кнопки "повесить трубку"
        hang_thread = threading.Thread(target=self._monitor_hang_button, daemon=True)
        hang_thread.start()

        # Поток для кнопки "вызов"
        call_thread = threading.Thread(target=self._monitor_call_button, daemon=True)
        call_thread.start()

        logger.info("Обработчики кнопок управления инициализированы")

    def _monitor_pick_button(self):
        """Мониторит нажатие кнопки поднятия трубки"""
        previous_state = GPIO.input(self.PICK_BUTTON_PIN)
        while True:
            current_state = GPIO.input(self.PICK_BUTTON_PIN)
            # Обнаружение нажатия (переход от HIGH к LOW)
            if previous_state == GPIO.HIGH and current_state == GPIO.LOW:
                self._on_pick_button_press()
                time.sleep(0.3)  # Антидребезг
            previous_state = current_state
            time.sleep(0.01)

    def _monitor_hang_button(self):
        """Мониторит нажатие кнопки повешения трубки"""
        previous_state = GPIO.input(self.HANG_BUTTON_PIN)
        while True:
            current_state = GPIO.input(self.HANG_BUTTON_PIN)
            # Обнаружение нажатия
            if previous_state == GPIO.HIGH and current_state == GPIO.LOW:
                self._on_hang_button_press()
                time.sleep(0.3)  # Антидребезг
            previous_state = current_state
            time.sleep(0.01)

    def _monitor_call_button(self):
        """Мониторит нажатие кнопки вызова"""
        previous_state = GPIO.input(self.CALL_BUTTON_PIN)
        while True:
            current_state = GPIO.input(self.CALL_BUTTON_PIN)
            # Обнаружение нажатия
            if previous_state == GPIO.HIGH and current_state == GPIO.LOW:
                self._on_call_button_press()
                time.sleep(0.3)  # Антидребезг
            previous_state = current_state
            time.sleep(0.01)

    def _on_pick_button_press(self):
        """Обработчик нажатия кнопки поднятия трубки"""
        logger.info("Нажата кнопка 'поднять трубку'")
        self.state = PhoneState.IDLE
        tone_player.play_idle_tone()
        print("=== ТРУБКА ПОДНЯТА ===")
        print("Состояние: ОЖИДАНИЕ ВВОДА НОМЕРА")

    def _on_hang_button_press(self):
        """Обработчик нажатия кнопки повешения трубки"""
        logger.info("Нажата кнопка 'повесить трубку'")
        self.reset()
        print("=== ТРУБКА ПОВЕШЕНА ===")
        print("Состояние: ТЕЛЕФОН ПОВЕШЕН")

    def _on_call_button_press(self):
        """Обработчик нажатия кнопки вызова"""
        if self._state == PhoneState.IDLE:
            logger.info("Нажата кнопка 'вызов'")
            tone_player.stop_all()

            self.state = PhoneState.CALL
            number = self.screen or ""
            ringing_tone = find_ringing_tone(number)

            if not ringing_tone:
                logger.warning(f"Не найдена мелодия звонка для номера: {number}")
                print(f"ПРЕДУПРЕЖДЕНИЕ: Не найдена мелодия звонка для {number}")
                self.reset()
                return

            logger.info(f"Воспроизведение мелодии звонка для {number}")
            print(f"ВЫЗОВ НОМЕРА: {number}")
            print(f"СТРАНА: {self._get_country_by_number(number)}")
            tone_player.play_pattern(ringing_tone)

    def _get_country_by_number(self, number: str) -> str:
        """Получает страну по номеру (для отображения)"""
        from utils import get_country_by_number

        country = get_country_by_number(number)
        return country or "Не определена"

    @property
    def screen(self) -> str:
        """Возвращает содержимое экрана"""
        return self._screen_content

    @screen.setter
    def screen(self, text: str):
        """Устанавливает содержимое экрана"""
        self._screen_content += text
        print(f"ЭКРАН: {self._screen_content}")
        logger.info(f"Экран обновлен: {self._screen_content}")

    @property
    def state(self) -> str:
        """Возвращает текущее состояние телефона"""
        return self._state.value

    @state.setter
    def state(self, new_state: PhoneState):
        """Устанавливает новое состояние телефона"""
        old_state = self._state.value
        self._state = new_state
        logger.info(f"Состояние телефона изменено: {old_state} -> {new_state.value}")
        print(f"СОСТОЯНИЕ: {new_state.value.upper()}")

    def reset(self):
        """Сбрасывает телефон в исходное состояние"""
        logger.info("Сброс телефона")
        self._state = PhoneState.HANG
        tone_player.stop_all()

        # Очистка экрана
        self._screen_content = ""
        print("ЭКРАН: (очищен)")

        logger.info("Телефон сброшен в исходное состояние")

    def start(self):
        """Запускает основной цикл телефона"""
        print("=== ЭМУЛЯТОР ТЕЛЕФОНА ЗАПУЩЕН ===")
        print("Доступные команды:")
        print("- Поднять трубку: нажмите кнопку на GPIO23")
        print("- Повесить трубку: нажмите кнопку на GPIO24")
        print("- Вызов: нажмите кнопку на GPIO25")
        print("- Цифровая клавиатура: используйте матричную клавиатуру")
        print("================================")

        try:
            # Основной цикл работает в фоновых потоках
            import signal

            signal.pause()  # Ожидание сигнала для завершения
        except KeyboardInterrupt:
            logger.info("Получен сигнал завершения")
            self.cleanup()

    def cleanup(self):
        """Очистка ресурсов"""
        logger.info("Очистка ресурсов телефона")
        tone_player.cleanup()
        if hasattr(self.numpad, "cleanup"):
            self.numpad.cleanup()
        GPIO.cleanup()
        print("=== РАБОТА ТЕЛЕФОНА ЗАВЕРШЕНА ===")