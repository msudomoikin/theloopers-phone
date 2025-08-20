# tone_player.py
import sounddevice as sd
import numpy as np
import threading
import time
import logging
from typing import List, Tuple, Optional

logger = logging.getLogger(__name__)


class ToneElement:
    def __init__(
        self, frequencies: List[int], modulated: bool, duration: int, no_repeat: bool
    ):
        self.frequencies = frequencies
        self.modulated = modulated
        self.duration = duration
        self.no_repeat = no_repeat


class TonePlayer:
    def __init__(self):
        self.sample_rate = 44100
        self.is_playing = False
        self.stream = None
        self.current_thread = None
        self.stop_event = threading.Event()

        # Для паттернов
        self.pattern_timeout = None
        self.current_pattern: List[ToneElement] = []
        self.pattern_index = 0
        self.should_repeat = True

        logger.info("Инициализация TonePlayer завершена")

    def _generate_sine_wave(
        self, frequency: float, duration: float, amplitude: float = 0.3
    ) -> np.ndarray:
        """Генерирует синусоидальную волну заданной частоты"""
        t = np.linspace(0, duration, int(self.sample_rate * duration), False)
        wave = amplitude * np.sin(2 * np.pi * frequency * t)
        return wave

    def _generate_dtmf_tone(
        self, freq1: float, freq2: float, duration: float
    ) -> np.ndarray:
        """Генерирует DTMF тон (две частоты одновременно)"""
        t = np.linspace(0, duration, int(self.sample_rate * duration), False)
        wave1 = 0.15 * np.sin(2 * np.pi * freq1 * t)
        wave2 = 0.15 * np.sin(2 * np.pi * freq2 * t)
        return wave1 + wave2

    def _generate_am_tone(
        self, carrier_freq: float, modulator_freq: float, duration: float
    ) -> np.ndarray:
        """Генерирует амплитудно-модулированный тон"""
        t = np.linspace(0, duration, int(self.sample_rate * duration), False)
        carrier = np.sin(2 * np.pi * carrier_freq * t)
        modulator = np.sin(2 * np.pi * modulator_freq * t)
        # Амплитудная модуляция: (1 + modulator) * carrier
        am_wave = 0.35 * (1 + 0.95 * modulator) * carrier
        return am_wave

    def _play_wave(self, wave: np.ndarray):
        """Воспроизводит волну через sounddevice"""
        try:
            # Плавное нарастание для предотвращения щелчков
            fade_samples = int(0.005 * self.sample_rate)  # 5ms fade
            if len(wave) > fade_samples * 2:
                fade_in = np.linspace(0, 1, fade_samples)
                fade_out = np.linspace(1, 0, fade_samples)
                wave[:fade_samples] *= fade_in
                wave[-fade_samples:] *= fade_out

            self.stop_event.clear()
            sd.play(wave, self.sample_rate, blocking=False)

            # Ждем завершения воспроизведения или остановки
            while sd.get_status() and not self.stop_event.is_set():
                time.sleep(0.01)

        except Exception as e:
            logger.error(f"Ошибка воспроизведения звука: {e}")

    def start(self, freq_array: Tuple[float, float]):
        """
        Запускает воспроизведение DTMF тона

        Args:
            freq_array: Кортеж из двух частот (freq1, freq2)
        """
        logger.info(f"Запуск DTMF тона: {freq_array[0]}, {freq_array[1]}")

        def play_thread():
            try:
                wave = self._generate_dtmf_tone(
                    freq_array[0], freq_array[1], 1.0
                )  # 1 секунда
                self._play_wave(wave)
            except Exception as e:
                logger.error(f"Ошибка в потоке воспроизведения: {e}")
            finally:
                self.is_playing = False

        self.stop_all()
        self.is_playing = True
        self.current_thread = threading.Thread(target=play_thread, daemon=True)
        self.current_thread.start()

    def stop_all(self):
        """Останавливает все воспроизведение"""
        logger.info("Остановка всех тонов")
        self.stop_event.set()

        if self.current_thread and self.current_thread.is_alive():
            self.current_thread.join(timeout=0.1)

        try:
            sd.stop()
        except:
            pass

        self.is_playing = False
        self.current_thread = None

    def play_idle_tone(self):
        """Воспроизводит тон ожидания (350Hz + 440Hz)"""
        logger.info("Воспроизведение тона ожидания")
        self.start((350, 440))

    def _parse_tone_pattern(self, pattern: str) -> List[ToneElement]:
        """Парсит строку паттерна в список элементов"""
        elements = pattern.split(",")
        tone_elements = []

        for element in elements:
            no_repeat = element.startswith("!")
            clean_element = element[1:] if no_repeat else element

            parts = clean_element.split("/")
            freq_part = parts[0]
            duration = int(parts[1]) if len(parts) > 1 and parts[1].isdigit() else 1000

            frequencies = []
            modulated = False

            if "*" in freq_part:
                # Модулированная частота (f1*f2)
                frequencies = [int(f) for f in freq_part.split("*")]
                modulated = True

tone_player_vanilla = TonePlayer()