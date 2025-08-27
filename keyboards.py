from telebot import types

def get_main_keyboard():
    """Основная клавиатура (старт/помощь)."""
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    buttons = [
        types.KeyboardButton("Подписать документ"),
        types.KeyboardButton("Помощь")
    ]
    markup.add(*buttons)
    return markup
