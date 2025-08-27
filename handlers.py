from telebot import types
import os
from config import STATES, SUPPORTED_FORMATS
from keyboards import get_main_keyboard
from operations import FileProcessor

class Handlers:
    def __init__(self, bot):
        self.bot = bot
        self.user_states = {}  # Хранит состояние каждого пользователя

    def handle_start(self, message):
        """Приветственное сообщение."""
        self.bot.reply_to(
            message,
            "Это бот для создания водяных знаков.\n"
            "Выберите действие ниже ",
            reply_markup=get_main_keyboard()
        )

    def handle_help(self, message):
        """Показывает справку."""
        help_text = """
<b>Как использовать бота:</b>
1. Нажмите <b>"Подписать документ"</b>
2. Отправьте файл <b>(PDF, DOC или DOCX)</b>
3. Отправьте текст для создания водяного знака \n
(если несколько, то каждый с новой строки)
4. Получите готовый(е) файл(ы)

<b>Поддерживаемые форматы:</b>
- PDF
- DOC
- DOCX
"""
        self.bot.send_message(message.chat.id, help_text, parse_mode="HTML")

    def handle_create_pdf(self, message):
        """Начинает процесс создания PDF"""
        self.user_states[message.chat.id] = {"state": STATES["WAITING_FOR_FILE"]}
        self.bot.send_message(
            message.chat.id,
            "Отправьте файл (PDF, DOC или DOCX):"
        )

    def process_file_step(self, message):
        """Обрабатывает загруженный файл"""
        chat_id = message.chat.id
        
        
        if not (message.document and message.document.file_name):
            msg = self.bot.send_message(chat_id, "Отправьте файл в формате PDF, DOC или DOCX:")
            self.bot.register_next_step_handler(msg, self.process_file_step)
            return
        
        file_ext = message.document.file_name.split('.')[-1].lower()
        if file_ext not in SUPPORTED_FORMATS:
            msg = self.bot.send_message(chat_id, "Неподдерживаемый формат. Нужен PDF, DOC или DOCX.")
            self.bot.register_next_step_handler(msg, self.process_file_step)
            return
        
        try:
            file_info = self.bot.get_file(message.document.file_id)
            downloaded_file = self.bot.download_file(file_info.file_path)
            
            temp_file_path = f"temp_{chat_id}.{file_ext}"
            with open(temp_file_path, 'wb') as new_file:
                new_file.write(downloaded_file)
            
            self.user_states[chat_id] = {
                "state": STATES["WAITING_FOR_STUDENTS"],
                "input_file": temp_file_path
            }
            
            self.bot.send_message(
                chat_id,
                f"Файл загружен! Отправьте текст водяного знака:",
            )
            
        except Exception as e:
            self.bot.reply_to(message, f"Ошибка: {str(e)}")
            self.cleanup_user_data(chat_id)

    def process_students_step(self, message):
        """Обрабатывает список и создает PDF"""
        chat_id = message.chat.id
        
        
        students = [s.strip() for s in message.text.split('\n') if s.strip()]
        
        if not students:
            msg = self.bot.send_message(chat_id, "Список пуст. Попробуйте снова:")
            self.bot.register_next_step_handler(msg, self.process_students_step)
            return
        
        input_file = self.user_states.get(chat_id, {}).get("input_file")
        

        self.bot.send_message(chat_id, "⏳ Подождите...")
        
        try:
            has_errors = False
            for result in FileProcessor.create_pdfs_for_students(students, input_file):
                if result.endswith('.pdf'):
                    with open(result, 'rb') as f:
                        self.bot.send_document(chat_id, f)
                    os.remove(result)
                else:
                    self.bot.send_message(chat_id, result)
                    has_errors = True
            
            if not has_errors:
                self.bot.send_message(chat_id, "✅ Готово", reply_markup=get_main_keyboard())
            else:
                self.bot.send_message(chat_id, "❌ Что-то пошло не так", reply_markup=get_main_keyboard())
                
        except Exception as e:
            self.bot.send_message(chat_id, f"{str(e)}")
        finally:
            self.cleanup_user_data(chat_id)

    def cleanup_user_data(self, chat_id):
        """Удаляет временные файлы."""
        if chat_id in self.user_states:
            temp_file = self.user_states[chat_id].get("input_file")
            if temp_file and os.path.exists(temp_file):
                try:
                    os.remove(temp_file)
                except:
                    pass
            del self.user_states[chat_id]