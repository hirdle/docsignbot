import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # Корневая директория

"""Пути к файлам"""
DEFAULT_INPUT_PDF = os.path.join(BASE_DIR, "default.pdf")  # Стандартный шаблон PDF
DEFAULT_OUTPUT_FOLDER = os.path.join(BASE_DIR, "output_pdfs")  # Папка для готовых PDF
FONTS_FOLDER = os.path.join(BASE_DIR, "fonts")  # Папка со шрифтами
ROBOTO_FONT = os.path.join(FONTS_FOLDER, "Roboto-Regular.ttf")  # Путь к шрифту Roboto
TEMP_FOLDER = os.path.join(BASE_DIR, "temp")  # Папка для временных файлов

"""Автоматическое создание папок"""
os.makedirs(DEFAULT_OUTPUT_FOLDER, exist_ok=True)
os.makedirs(FONTS_FOLDER, exist_ok=True)
os.makedirs(TEMP_FOLDER, exist_ok=True)

"""Поддерживаемые форматы файлов"""
SUPPORTED_FORMATS = {
    'pdf': 'application/pdf',
    'doc': 'application/msword',
    'docx': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
}

"""Состояния бота"""
STATES = {
    "WAITING_FOR_FILE": 1,      # Ожидание файла
    "WAITING_FOR_STUDENTS": 2   # Ожидание списка учеников
}
