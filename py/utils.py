# utils.py
import re
import logging
from phonebook import phonebook_records, PhonebookRecord

logger = logging.getLogger(__name__)


def find_ringing_tone(number: str) -> str | None:
    """
    Находит мелодию звонка для заданного номера телефона

    Args:
        number (str): Номер телефона

    Returns:
        str | None: Строка мелодии звонка или None если не найдена
    """
    logger.debug(f"Поиск мелодии звонка для номера: {number}")

    for record in phonebook_records:
        if record.code and re.match(record.code, number):
            logger.debug(f"Найдена мелодия звонка: {record.ring_tone}")
            return record.ring_tone

    logger.warning(f"Мелодия звонка не найдена для номера: {number}")
    return None


def is_touch_device() -> bool:
    """
    Проверяет, является ли устройство сенсорным.
    Для Raspberry Pi всегда возвращает False, так как это стационарное устройство.

    Returns:
        bool: True если устройство сенсорное, False в противном случае
    """
    # На Raspberry Pi это всегда False, так как нет сенсорного экрана
    return False


def format_phone_number(number: str) -> str:
    """
    Форматирует номер телефона для отображения

    Args:
        number (str): Номер телефона

    Returns:
        str: Отформатированный номер телефона
    """
    # Убираем все нецифровые символы
    clean_number = re.sub(r"\D", "", number)

    # Форматируем в зависимости от длины
    if len(clean_number) == 11 and clean_number.startswith("7"):
        # Российский формат: +7 (XXX) XXX-XXXX
        return f"+7 ({clean_number[1:4]}) {clean_number[4:7]}-{clean_number[7:]}"
    elif len(clean_number) == 10:
        # Формат: (XXX) XXX-XXXX
        return f"({clean_number[:3]}) {clean_number[3:6]}-{clean_number[6:]}"
    else:
        return clean_number


def validate_phone_number(number: str) -> bool:
    """
    Проверяет валидность номера телефона

    Args:
        number (str): Номер телефона

    Returns:
        bool: True если номер валидный, False в противном случае
    """
    # Убираем все нецифровые символы
    clean_number = re.sub(r"\D", "", number)

    # Проверяем длину (минимум 3 цифры, максимум 15)
    if len(clean_number) < 3 or len(clean_number) > 15:
        return False

    # Проверяем, что состоит только из цифр
    return clean_number.isdigit()


def get_country_by_number(number: str) -> str | None:
    """
    Возвращает страну по номеру телефона

    Args:
        number (str): Номер телефона

    Returns:
        str | None: Название страны или None если не найдена
    """
    for record in phonebook_records:
        if record.code and re.match(record.code, number):
            return record.country
    return None
