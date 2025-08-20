# main.py
from phone import Phone
from phonebook import Phonebook
import logging

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def main():
    logger.info("Инициализация телефона...")

    # Создаем экземпляр телефона
    phone = Phone()
    phonebook = Phonebook()

    # Выводим телефонную книгу в консоль
    logger.info("Загрузка телефонной книги...")
    phonebook.render()  # Рендерим в консоль

    # Запуск основного цикла телефона
    phone.start()


if __name__ == "__main__":
    main()