# phonebook.py
import re
import logging

logger = logging.getLogger(__name__)

class PhonebookRecord:
    def __init__(self, country: str, flag_url: str, ring_tone: str, busy_tone: str, 
                 countries: list[str] = None, code: str = None):
        self.country = country
        self.flag_url = flag_url
        self.ring_tone = ring_tone
        self.busy_tone = busy_tone
        self.countries = countries or []
        self.code = code

# Данные телефонной книги
PHONEBOOK_RECORDS = [
    PhonebookRecord(
        country='Russia',
        countries=['Kyrgyzstan', 'Lithuania', 'Moldova', 'Russia', 'Tajikistan'],
        flag_url='https://upload.wikimedia.org/wikipedia/commons/f/f3/Flag_of_Russia.svg',
        ring_tone="425/800,0/3200",
        busy_tone='',
        code=r'^7'
    ),
    PhonebookRecord(
        country='Jamaica',
        countries=['Antigua and Barbuda', 'Bahamas', 'Barbados', 'Bermuda', 'British Virgin Islands', 
                  'Canada', 'Cuba', 'Dominica', 'Grenada', 'Jamaica', 'Montserrat', 'Saint Kitts and Nevis', 
                  'Trinidad and Tobago', 'Turks and Caicos Islands', 'USA'],
        flag_url='https://upload.wikimedia.org/wikipedia/commons/0/0a/Flag_of_Jamaica.svg',
        ring_tone="440+480/2000,0/4000",
        busy_tone='',
        code=r'^1'
    ),
    PhonebookRecord(
        country='Australia',
        countries=['Fiji', 'Nauru'],
        flag_url='https://upload.wikimedia.org/wikipedia/commons/b/b9/Flag_of_Australia.svg',
        ring_tone="425*25/400,0/200,425*25/400,0/2000",
        busy_tone='',
        code=r'^61'
    ),
    PhonebookRecord(
        country='Japan',
        countries=[],
        flag_url='https://upload.wikimedia.org/wikipedia/commons/9/9e/Flag_of_Japan.svg',
        ring_tone="400*16/1000,0/2000",
        busy_tone='',
        code=r'^81'
    ),
    PhonebookRecord(
        country='India',
        countries=['India', 'Bhutan'],
        flag_url='https://upload.wikimedia.org/wikipedia/commons/4/41/Flag_of_India.svg',
        ring_tone="400*25/400,0/200,400*25/400,0/2600",
        busy_tone='',
        code=r'^91'
    ),
    PhonebookRecord(
        country='Austria',
        countries=['Germany'],
        flag_url='https://upload.wikimedia.org/wikipedia/commons/4/41/Flag_of_Austria.svg',
        ring_tone="450/1000,0/5000",
        busy_tone='',
        code=r'^43'
    ),
    PhonebookRecord(
        country='Serbia',
        countries=[],
        flag_url='https://upload.wikimedia.org/wikipedia/commons/f/ff/Flag_of_Serbia.svg',
        ring_tone="450*25/1000,0/9000",
        busy_tone='',
        code=r'^381'
    ),
    PhonebookRecord(
        country='Guinea',
        countries=[],
        flag_url='https://upload.wikimedia.org/wikipedia/commons/e/ed/Flag_of_Guinea.svg',
        ring_tone="450/400,0/200",
        busy_tone='',
        code=r'^224'
    ),
    PhonebookRecord(
        country='Pakistan',
        countries=[],
        flag_url='https://upload.wikimedia.org/wikipedia/commons/3/32/Flag_of_Pakistan.svg',
        ring_tone="400/1000,0/2000",
        busy_tone='',
        code=r'^92'
    )
]

class Phonebook:
    def __init__(self):
        pass
    
    def render(self):
        """Выводит телефонную книгу в консоль"""
        logger.info("Рендеринг телефонной книги:")
        print("\n=== ТЕЛЕФОННАЯ КНИГА ===")
        
        for record in PHONEBOOK_RECORDS:
            # Извлекаем код страны из регулярного выражения для отображения
            code_display = record.code.replace('^', '').replace('$', '') if record.code else ''
            
            print(f"\nСтрана: {record.country}")
            print(f"  Код: {code_display}")
            print(f"  Флаг: {record.flag_url}")
            print(f"  Мелодия звонка: {record.ring_tone}")
            
            if record.countries:
                print(f"  Страны: {', '.join(record.countries)}")
        
        print("\n========================\n")
    
    def get_record_by_number(self, phone_number: str) -> PhonebookRecord:
        """
        Возвращает запись телефонной книги по номеру телефона
        
        Args:
            phone_number (str): Номер телефона
            
        Returns:
            PhonebookRecord: Запись телефонной книги или None
        """
        for record in PHONEBOOK_RECORDS:
            if record.code and re.match(record.code, phone_number):
                return record
        return None
    
    def get_all_records(self) -> list[PhonebookRecord]:
        """Возвращает все записи телефонной книги"""
        return PHONEBOOK_RECORDS.copy()

# Экспорт данных для использования в других модулях
phonebook_records = PHONEBOOK_RECORDS