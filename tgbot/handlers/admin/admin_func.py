from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext

from tgbot.handlers.buttons import show_button
from tgbot.states.user_states import StatesAdmin
from tgbot.utiles.database.firebase import create_book
from tgbot.utiles.questions.parsing import parse
from tgbot.utiles.help_func.custom_exception import *


async def add_book(message: types.Message, state: FSMContext):
    await message.answer("Отправьте страницу с книгой, которую хотите добавить, с сайта www.Litres.ru. Убедитесь, что "
                         "на странице присутствуют Оглавление, ISBN, Автор и Дата перевода/написания, а также "
                         "количество страниц. Страница не должна содержать аудиокнигу.",
                         reply_markup=show_button(["Отмена"]))
    await state.set_state(StatesAdmin.add_book_url)


async def add_book_in_database(message: types.Message,  state: FSMContext):
    if message.text == "Отмена":
        await message.answer("Вы вышли в меню админ-панели.",
                             reply_markup=show_button(["Добавить книгу", "Добавить вопрос"]))
        await state.set_state(StatesAdmin.admin)
    else:
        url = message.text

        await state.set_state(StatesAdmin.add_book_waiting)
        await message.answer('Подождите. Идёт создание книги в Базе Данных.')

        try:
            content_sheet, info = parse(url)
            await create_book(content_sheet, info)
            await message.answer('Данные успешно отправлены.',
                                 reply_markup=show_button(["Добавить книгу", "Добавить вопрос"]))
            await state.set_state(StatesAdmin.admin)
        except ErrorSendData:
            await message.answer('Ошибка отправки данных. Попробуйте отправить позже, либо напишите администратору.',
                                 reply_markup=show_button(["Добавить книгу", "Добавить вопрос"]))
            await state.set_state(StatesAdmin.admin)
        except ErrorTableOfContentEmpty:
            await message.answer("Ошибка парсинга страницы. На данной странице отсутствует оглавление."
                                 "\nОтправьте другую ссылку.",
                                 reply_markup=show_button(["Отмена"]))
            await state.set_state(StatesAdmin.add_book_url)
        except ErrorParsePage:
            await message.answer("Ошибка парсинга страницы. Проверьте есть ли на этой странице оглавление и убедитесь, "
                                 "что остальная информация о книге корректна. На странице должны присутствовать: "
                                 "'Оглавление', 'Автор', 'Объем', 'Дата перевода' или 'Дата написания', "
                                 "а также ISBN. \nОтправьте другую ссылку.",
                                 reply_markup=show_button(["Отмена"]))
            await state.set_state(StatesAdmin.add_book_url)


def register_commands(dp: Dispatcher):
    dp.register_message_handler(add_book, text="Добавить книгу", state=StatesAdmin.admin)
    dp.register_message_handler(add_book_in_database,
                                content_types=types.ContentType.TEXT,
                                state=StatesAdmin.add_book_url)
