from aiogram import types


def show_button(list_menu):
    """Принимает список и превращает его в кнопки"""
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*list_menu)
    return keyboard