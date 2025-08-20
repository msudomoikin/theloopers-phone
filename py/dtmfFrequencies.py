# dtmf_frequencies.py


def get_dtmf_frequency(button_text: str) -> tuple[int, int]:
    """
    Возвращает частоты DTMF для заданной кнопки.

    Args:
        button_text (str): Символ кнопки ('0'-'9', '*', '#')

    Returns:
        tuple[int, int]: Кортеж из двух частот (row_freq, col_freq)
    """
    frequency_map = {
        "1": (697, 1209),
        "2": (697, 1336),
        "3": (697, 1477),
        "4": (770, 1209),
        "5": (770, 1336),
        "6": (770, 1477),
        "7": (852, 1209),
        "8": (852, 1336),
        "9": (852, 1477),
        "*": (941, 1209),
        "0": (941, 1336),
        "#": (941, 1477),
    }

    return frequency_map.get(button_text, (440, 440))
