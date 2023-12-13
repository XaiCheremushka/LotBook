from aiogram import types


def show_button(list_menu):
    """Принимает список и превращает его в кнопки"""
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*list_menu)
    return keyboard


def show_inline_buttons(list_names):

    buttons = [types.InlineKeyboardButton(name, callback_data=name) for name in list_names]
    buttonLeft = types.InlineKeyboardButton()

    inline_keyboard = types.InlineKeyboardMarkup(row_width=1)
    inline_keyboard.add(*buttons)
    inline_keyboard.row()

    return inline_keyboard

