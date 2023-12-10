# import re
#
# from aiogram import types, Dispatcher, Bot
# from aiogram.dispatcher import FSMContext
# from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
#
# from tgbot.handlers.buttons import show_inline_buttons
# from tgbot.utiles.database.firebase import get_all_names_of_books, get_all_sections_of_book
# from tgbot.states.user_states import StatesAdmin
# from tgbot.utiles.secretData.config import config
#
# bot = Bot(token=config.BOT_TOKEN.get_secret_value())
#
#
#
# # async def show_books_and_sections(message, start_index=0):
# #     global current_sections
# #
# #     if current_sections is None:
# #         items = books[start_index:start_index + 10]
# #         inline_keyboard = InlineKeyboardMarkup(row_width=1)
# #         for item in items:
# #             button = InlineKeyboardButton(text=item["title"], callback_data=f"book_{item['title']}")
# #             inline_keyboard.add(button)
# #
# #         # Добавляем кнопки для навигации
# #         if start_index + 10 < len(books):
# #             next_button = InlineKeyboardButton(text="Next", callback_data=f"next_{start_index + 10}")
# #             inline_keyboard.add(next_button)
# #
# #         if start_index - 10 >= 0:
# #             prev_button = InlineKeyboardButton(text="Previous", callback_data=f"prev_{start_index - 10}")
# #             inline_keyboard.add(prev_button)
# #
# #         await bot.send_message(message.chat.id, "Choose a book:", reply_markup=inline_keyboard)
# #     else:
# #         current_book = next((book for book in books if book["title"] == current_sections), None)
# #         if current_book:
# #             inline_keyboard = InlineKeyboardMarkup(row_width=1)
# #             for section in current_book["sections"]:
# #                 button = InlineKeyboardButton(text=section, callback_data=f"section_{section}")
# #                 inline_keyboard.add(button)
# #
# #             # Добавляем кнопку для возврата к выбору книг
# #             back_button = InlineKeyboardButton(text="Back to Books", callback_data="back_to_books")
# #             inline_keyboard.add(back_button)
# #
# #             await bot.send_message(message.chat.id, f"Choose a section of {current_sections}:", reply_markup=inline_keyboard)
# #         else:
# #             await bot.send_message(message.chat.id, "Book not found.")
#
#
# async def change_inline_keyboard(callback_query, state: FSMContext):
#     user_data = await state.get_data()
#     message_id = user_data.get("message_id")
#     start_index = user_data.get("start_index")
#     book_names = user_data.get("book_names")
#
#     if start_index == 0:
#         buttons = [InlineKeyboardButton(book, callback_data=f"book_{book}")
#                    for book in book_names[start_index:20]]
#         inline_keyboard = types.InlineKeyboardMarkup(row_width=1)
#         inline_keyboard.add(*buttons)
#         inline_keyboard.row(InlineKeyboardButton("⬅️", callback_data="left_arrow"))
#         if len(book_names) > 20:
#             inline_keyboard.row(InlineKeyboardButton("➡️", callback_data="right_arrow"))
#
#
# """Вызов первой команды"""
# async def add_question(message: types.Message, state: FSMContext):
#     book_names = await get_all_names_of_books()
#
#     buttons = [InlineKeyboardButton(book, callback_data="book_" + re.sub(r'\W+', '', book)) for book in book_names[:10]]
#
#     inline_keyboard = InlineKeyboardMarkup(row_width=1)
#     inline_keyboard.add(*buttons)
#     if len(book_names) > 10:
#         inline_keyboard.row(InlineKeyboardButton("➡️", callback_data="right_arrow"))
#
#     sent_message = await message.answer("Выберите книгу:", reply_markup=inline_keyboard)
#     await state.update_data(message_id=sent_message.message_id,
#                             start_index=0,
#                             book_names=book_names)
#     await state.set_state(StatesAdmin.add_question_choice_book)
#
#
# """Обработка нажатий при выборе книги"""
# async def callback_book(callback_query: types.CallbackQuery, state: FSMContext):
#     book = callback_query.data
#     user_data = await state.get_data()
#     message_id = user_data.get("message_id")
#     sections = await get_all_sections_of_book(book)
#
#     buttons = [types.InlineKeyboardButton(book, callback_data="section_" + re.sub(r'\W+', '', section)) for section in sections[:10]]
#
#     inline_keyboard = types.InlineKeyboardMarkup(row_width=1)
#     inline_keyboard.add(*buttons)
#     if len(sections) > 10:
#         inline_keyboard.row(InlineKeyboardButton("➡️", callback_data="right_arrow"))
#
#
# async def callback_book_next_page(callback_query: types.CallbackQuery, state: FSMContext):
#     user_data = await state.get_data()
#     message_id = user_data.get("message_id")
#     start_index = user_data.get("start_index")
#     book_names = user_data.get("book_names")
#
#     if start_index == 0:
#         buttons = [InlineKeyboardButton(book, callback_data=f"book_{book}")
#                    for book in book_names[start_index:20]]
#         inline_keyboard = types.InlineKeyboardMarkup(row_width=1)
#         inline_keyboard.add(*buttons)
#         inline_keyboard.row(InlineKeyboardButton("⬅️", callback_data="left_arrow"))
#         if len(book_names) > 20:
#             inline_keyboard.row(InlineKeyboardButton("➡️", callback_data="right_arrow"))
#
#
#
# def register_commands(dp: Dispatcher):
#     dp.register_message_handler(add_question, text="Добавить вопрос", state=StatesAdmin.admin)
#     dp.register_callback_query_handler(callback_book,
#                                        state=StatesAdmin.add_question_choice_book)
#     dp.register_callback_query_handler(callback_book_next_page,
#                                        text="right_arrow",
#                                        state=StatesAdmin.add_question_choice_book)


# from aiogram import types, Dispatcher
# from aiogram.dispatcher import FSMContext
# from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
# from aiogram.utils.callback_data import CallbackData
#
# from tgbot.utiles.database.firebase import (get_all_names_of_books, get_all_sections_1_of_book,
#                                             get_all_sections_2_of_book, get_all_sections_3_of_book, ErrorGetSectionData)
# from tgbot.states.user_states import StatesAdmin
#
# book_callback = CallbackData("book", "name")
# section_1_callback = CallbackData("section_1", "name", "section_1")
# section_2_callback = CallbackData("section_2", "name", "section_1", "section_2")
# section_3_callback = CallbackData("section_3", "name", "section_1", "section_2", "section_3")
#
#
# async def show_books(message: types.Message):
#     books = await get_all_names_of_books()
#     buttons = [
#         InlineKeyboardButton(text=book, callback_data=book_callback.new(name=book))
#         for book in books
#     ]
#     markup = InlineKeyboardMarkup(row_width=1)
#     markup.add(*buttons)
#     await message.answer("Выберите книгу:", reply_markup=markup)
#
#
# async def show_sections_1(callback: types.CallbackQuery, callback_data: dict, state: FSMContext):
#     name = callback_data["name"]
#     try:
#         sections = await get_all_sections_1_of_book(name)
#         buttons = [
#             InlineKeyboardButton(text=section, callback_data=section_1_callback.new(name=name, section_1=section))
#             for section in sections
#         ]
#         markup = InlineKeyboardMarkup(row_width=1)
#         markup.add(*buttons)
#         await callback.message.edit_text("Выберите раздел:", reply_markup=markup)
#     except ErrorGetSectionData:
#         await callback.message.answer("Как вы хотите добавить вопрос?")
#
#
# async def show_sections_2(callback: types.CallbackQuery, callback_data: dict, state: FSMContext):
#     name = callback_data["name"]
#     section_1 = callback_data["section_1"]
#     try:
#         sections = await get_all_sections_2_of_book(name, section_1)
#         buttons = [
#             InlineKeyboardButton(text=section, callback_data=section_2_callback.new(name=name, section_1=section_1, section_2=section))
#             for section in sections
#         ]
#         markup = InlineKeyboardMarkup(row_width=1)
#         markup.add(*buttons)
#         await callback.message.edit_text("Выберите подраздел:", reply_markup=markup)
#     except ErrorGetSectionData:
#         await callback.message.answer("Как вы хотите добавить вопрос?")
#
#
# async def show_sections_3(callback: types.CallbackQuery, callback_data: dict, state: FSMContext):
#     name = callback_data["name"]
#     section_1 = callback_data["section_1"]
#     section_2 = callback_data["section_2"]
#     try:
#         sections = await get_all_sections_3_of_book(name, section_1, section_2)
#         buttons = [
#             InlineKeyboardButton(text=section, callback_data=section_3_callback.new(name=name, section_1=section_1, section_2=section_2, section_3=section))
#             for section in sections
#         ]
#         markup = InlineKeyboardMarkup(row_width=1)
#         markup.add(*buttons)
#         await callback.message.edit_text("Выберите подраздел:", reply_markup=markup)
#     except ErrorGetSectionData:
#         await callback.message.answer("Как вы хотите добавить вопрос?")
#
#
# async def start_over(callback: types.CallbackQuery, callback_data: dict, state: FSMContext):
#     await show_books(callback.message)
#
#
# async def navigation_callback(callback: types.CallbackQuery, callback_data: dict, state: FSMContext):
#     current_page = int(callback_data["page"])
#     if callback_data["direction"] == "next":
#         current_page += 1
#     else:
#         current_page -= 1
#
#     if current_page < 1:
#         current_page = 1
#
#     # Implement logic to determine the maximum number of pages
#     max_pages = 2  # Set your maximum number of pages here
#
#     if current_page > max_pages:
#         current_page = max_pages
#
#     await callback.message.edit_text(f"Page {current_page}")
#
#
# def register_commands(dp: Dispatcher):
#     # Зарегистрируем команды в диспетчере
#     # dp.register_message_handler(show_books, lambda c: c.data == "show_books")
#     dp.register_message_handler(show_books, text="Добавить вопрос", state=StatesAdmin.admin)
#     dp.register_callback_query_handler(show_sections_1, book_callback.filter())
#     dp.register_callback_query_handler(show_sections_2, section_1_callback.filter())
#     dp.register_callback_query_handler(show_sections_3, section_2_callback.filter())
#     # dp.register_callback_query_handler(start_over, section_3_callback.filter())
#     dp.register_callback_query_handler(navigation_callback, lambda c: c.data.startswith("navigation"))


# from aiogram import types, Dispatcher
# from aiogram.dispatcher import FSMContext
#
# from tgbot.handlers.buttons import show_button
# from tgbot.utiles.database import firebase
# from tgbot.states.user_states import StatesAdmin
#
#
# async def add_question_start(message: types.Message, state: FSMContext):
#     books = await firebase.get_all_names_of_books()
#     await message.answer('Выберите книгу: \n"' + '"\n"'.join(books) + '"', reply_markup=show_button(["Отмена"]))
#     await state.set_state(StatesAdmin.add_question_choice_book)
#
#
# async def choice_book(message: types.Message, state: FSMContext):
#     if message.text == "Отмена":
#         await message.answer('Выберите нужную команду', reply_markup=show_button(["Добавить книгу", "Добавить вопрос"]))
#         await state.set_state(StatesAdmin.admin)
#     else:
#         book = message.text
#         sections = await firebase.get_all_sections_1_of_book(book)
#         await message.answer('Выберите раздел: \n"' + '"\n"'.join(sections) + '"', reply_markup=show_button(["Отмена"]))
#         await state.set_state(StatesAdmin.add_question_choice_section_1)
#
#
#
# def register_commands(dp: Dispatcher):
#     dp.register_message_handler(add_question_start, text="Добавить вопрос", state=StatesAdmin.admin)
#     dp.register_message_handler(choice_book, state=StatesAdmin.add_question_choice_book)



from aiogram import types, Dispatcher, Bot
from aiogram.dispatcher import FSMContext
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from tgbot.handlers.buttons import show_button
from tgbot.utiles.database import firebase
from tgbot.states.user_states import StatesAdmin
from tgbot.utiles.help_func.custom_exception import *
from tgbot.utiles.questions import chatGPT as gpt
from tgbot.utiles.secretData.config import config

bot = Bot(token=config.BOT_TOKEN.get_secret_value())

async def add_question_start(message: types.Message, state: FSMContext):
    """
    Функция add_question_start отображает инлайн-кнопки с выбором книги.
    """

    books = await firebase.get_all_names_of_books()

    buttons = [InlineKeyboardButton(books[i], callback_data=f"book_{i+1}") for i in range(0, len(books))]
    inline_keyboard = InlineKeyboardMarkup(row_width=1)
    inline_keyboard.add(*buttons)


    sent_message = await message.answer('Выберите книгу: ', reply_markup=inline_keyboard)
    await state.update_data(message_id=sent_message.message_id,
                            books=books)
    await state.set_state(StatesAdmin.add_question_choice)


async def choice_book(callback_query: types.CallbackQuery, state: FSMContext):
     """
     Функция choice_book реагирует на нажатие инлайн-кнопки с книгой и
     меняет все кнопки на кнопки с разделами этой книги.
     """
     user_data = await state.get_data()

     books = user_data.get("books")
     book = books[int(callback_query.data.replace("book_", "")) - 1]

     message_id = user_data.get("message_id")
     chat_id = callback_query.from_user.id
     sections = await firebase.get_all_sections_1_of_book(book)

     buttons = [types.InlineKeyboardButton(sections[i],
                                           callback_data=f"section_{i+1}") for i in range(0, len(sections))]

     inline_keyboard = types.InlineKeyboardMarkup(row_width=1)
     inline_keyboard.add(*buttons)

     await state.update_data(book=book, sections=sections)
     await bot.edit_message_reply_markup(chat_id=chat_id, message_id=message_id, reply_markup=inline_keyboard)
     # await state.set_state(StatesAdmin.add_question_choice_section_1)


async def choice_section_1(callback_query: types.CallbackQuery, state: FSMContext):
    """
    Функция choice_section_1 реагирует на нажатие инлайн-кнопки с разделом книги и если в этом разделе есть подразделы,
    то меняет кнопки на кнопки с подразделами.
    """
    user_data = await state.get_data()
    sections = user_data.get("sections")

    section_1 = sections[int(callback_query.data.replace("section_", "")) - 1]
    book = user_data.get("book")
    message_id = user_data.get("message_id")
    chat_id = callback_query.from_user.id

    try:
        subsections = await firebase.get_all_sections_2_of_book(book, section_1)
        buttons = [types.InlineKeyboardButton(subsections[i],
                                              callback_data=f"subsection_{i + 1}") for i in range(0, len(subsections))]

        inline_keyboard = types.InlineKeyboardMarkup(row_width=1)
        inline_keyboard.add(*buttons)

        await state.update_data(section_1=section_1, subsections=subsections)
        await bot.edit_message_reply_markup(chat_id=chat_id, message_id=message_id, reply_markup=inline_keyboard)
    except ErrorGetSectionData:
        print("348")
        await state.reset_data()
        await state.update_data(book=book, section_1=section_1)
        await bot.delete_message(chat_id=chat_id, message_id=message_id)
        await bot.send_message(chat_id=chat_id,
                               text=f'Раздел: "{section_1}"\nВведите вопрос: ', reply_markup=show_button([]))
        await state.set_state(StatesAdmin.add_question_name)


async def choice_section_2(callback_query: types.CallbackQuery, state: FSMContext):
    """
    Функция choice_section_2 реагирует на нажатие инлайн-кнопки с подразделом книги и если в этом разделе есть
    дополнительные подразделы, то меняет кнопки на кнопки с дополнительными подразделами.
    """
    user_data = await state.get_data()
    subsections = user_data.get("subsections")

    book = user_data.get("book")
    section_1 = user_data.get("section_1")
    section_2 = subsections[int(callback_query.data.replace("subsection_", "")) - 1]
    message_id = user_data.get("message_id")
    chat_id = callback_query.from_user.id

    try:
        sub_subsections = await firebase.get_all_sections_3_of_book(book, section_1, section_2)
        buttons = [InlineKeyboardButton(sub_subsections[i],
                                        callback_data=f"sub_subsection_{i + 1}") for i in range(0, len(sub_subsections))]

        inline_keyboard = InlineKeyboardMarkup(row_width=1)
        inline_keyboard.add(*buttons)

        await state.update_data(section_2=section_2, sub_subsections=sub_subsections)
        await bot.edit_message_reply_markup(chat_id=chat_id, message_id=message_id, reply_markup=inline_keyboard)
    except ErrorGetSectionData:
        await state.reset_data()
        await state.update_data(book=book, section_1=section_1, section_2=section_2)
        await bot.delete_message(chat_id=chat_id, message_id=message_id)
        await bot.send_message(chat_id=chat_id,
                               text=f'Подраздел: "{section_2}"\nВведите вопрос: ', reply_markup=show_button([]))
        await state.set_state(StatesAdmin.add_question_name)


async def choice_section_3(callback_query: types.CallbackQuery, state: FSMContext):
    """
    Функция choice_section_3 реагирует на нажатие инлайн-кнопки с дополнительным подразделом книги и
    если в этом разделе есть дополнительные под-подразделы, то меняет кнопки на кнопки с
    дополнительными под-подразделами.
    """
    user_data = await state.get_data()
    sub_subsections = user_data.get("sub_subsections")

    book = user_data.get("book")
    section_1 = user_data.get("section_1")
    section_2 = user_data.get("section_2")
    section_3 = sub_subsections[int(callback_query.data.replace("sub_subsection_", "")) - 1]
    message_id = user_data.get("message_id")
    chat_id = callback_query.from_user.id

    try:
        """Если необходимо, то можно увеличить распознавание вложенности, но при этом нужно её также увеличить и в
        firebase.create_book в дереве создания оглавления"""
        pass
        # sub_subsections = await firebase.get_all_sections_3_of_book(book, section_1, section_2)
        # buttons = [types.InlineKeyboardButton(sub_subsections[i],
        #                                       callback_data=f"sub_subsection_{i + 1}") for i in range(0, len(sub_subsections))]
        #
        # inline_keyboard = types.InlineKeyboardMarkup(row_width=1)
        # inline_keyboard.add(*buttons)
        #
        # await state.update_data(section_2=section_2, sub_subsections=sub_subsections)
        # await bot.edit_message_reply_markup(chat_id=chat_id, message_id=message_id, reply_markup=inline_keyboard)
    except ErrorGetSectionData:
        await state.reset_data()
        await state.update_data(book=book, section_1=section_1, section_2=section_2, section_3=section_3)
        await bot.delete_message(chat_id=chat_id, message_id=message_id)
        await bot.send_message(chat_id=chat_id,
                               text=f'Раздел подраздела: "{section_3}"\nВведите вопрос: ', reply_markup=show_button([]))
        await state.set_state(StatesAdmin.add_question_name)


async def add_question_name(message: types.Message, state: FSMContext):
    await state.update_data(question=message.text)
    await message.answer("Введите правильный ответ:")
    await state.set_state(StatesAdmin.add_question_true_answer)


async def add_question_true_answer(message: types.Message, state: FSMContext):
    await state.update_data(true_answer=message.text, false_answers_num=0)

    inline_keyboard = InlineKeyboardMarkup()
    inline_keyboard.add(InlineKeyboardButton("Самому", callback_data="himself"))
    inline_keyboard.add(InlineKeyboardButton("ChatGPT", callback_data="chatGPT"))

    sent_message = await message.answer("Выберите вариант создания остальных ответов", reply_markup=inline_keyboard)
    message_id = sent_message.message_id
    await state.update_data(message_id=message_id)
    await state.set_state(StatesAdmin.add_question_choice_create_answers)


async def add_question_chatGPT(callback_query: types.CallbackQuery, state: FSMContext):
    user_data = await state.get_data()
    book = user_data.get("book")
    question = user_data.get("question")
    true_answer = user_data.get("true_answer")

    chatGPT_result = await gpt.create_answers(book, question, true_answer)
    false_answers = chatGPT_result.split("\n")
    false_answers = [false_answer[3:] for false_answer in false_answers]

    inline_keyboard = InlineKeyboardMarkup()
    inline_keyboard.add(InlineKeyboardButton("Ещё", callback_data=f"chatGPT"))
    inline_keyboard.add(InlineKeyboardButton("Добавить", callback_data="add"))
    inline_keyboard.add(InlineKeyboardButton("Отмена", callback_data="cancel"))

    await bot.delete_message(chat_id=callback_query.from_user.id, message_id=user_data.get("message_id"))
    sent_message = await bot.send_message(chat_id=callback_query.from_user.id,
                                          text=f"Сгенерированные варианты: \n{question}\n{true_answer}\n"
                                               f"{false_answers[0]}\n{false_answers[1]}\n{false_answers[2]}",
                                          reply_markup=inline_keyboard)
    message_id = sent_message.message_id
    await state.update_data(message_id=message_id, false_answer_1=false_answers[0],
                            false_answer_2=false_answers[1], false_answer_3=false_answers[2])


async def add_question_add_in_database(callback_query: types.CallbackQuery, state: FSMContext):
    user_data = await state.get_data()
    book = user_data.get("book")
    section_1 = user_data.get("section_1")
    section_2 = user_data.get("section_2") if "section_2" in user_data else None
    section_3 = user_data.get("section_3") if "section_3" in user_data else None
    question = user_data.get("question")
    answers = [user_data.get("true_answer")] + [user_data.get(f"false_answer_{i}") for i in range(1, 4)]

    await bot.delete_message(chat_id=callback_query.from_user.id,
                             message_id=user_data.get("message_id"))
    try:
        await firebase.set_question(book, question, answers, section_1, section_2, section_3)
        await bot.send_message(chat_id=callback_query.from_user.id,
                               text="Вопрос успешно добавлен")
        await bot.send_message(chat_id=callback_query.from_user.id,
                               text="Выберите нужную команду",
                               reply_markup=show_button(["Добавить книгу", "Добавить вопрос"]))
        await state.reset_data()
        await state.set_state(StatesAdmin.admin)
    except ErrorSendData:
        await bot.send_message(chat_id=callback_query.from_user.id,
                               text="Не удалось отправить данные.")
        await bot.send_message(chat_id=callback_query.from_user.id,
                               text="Выберите нужную команду",
                               reply_markup=show_button(["Добавить книгу", "Добавить вопрос"]))
        await state.reset_data()
        await state.set_state(StatesAdmin.admin)


async def add_question_cancel(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.send_message(chat_id=callback_query.from_user.id,
                           text="Выберите нужную команду",
                           reply_markup=show_button(["Добавить книгу", "Добавить вопрос"]))
    await state.reset_data()
    await state.set_state(StatesAdmin.admin)


async def add_question_himself(callback_query: types.CallbackQuery, state: FSMContext):
    user_data = await state.get_data()
    await bot.delete_message(chat_id=callback_query.from_user.id, message_id=user_data.get("message_id"))
    await bot.send_message(chat_id=callback_query.from_user.id,
                           text="Необходимо ввести 3 неправильных ответа. \nВведите первый неправильный ответ:")
    await state.set_state(StatesAdmin.add_question_false_answer)


async def add_question_false_answers(message: types.Message, state: FSMContext):
    user_data = await state.get_data()
    false_answers_num = int(user_data.get("false_answers_num"))
    if false_answers_num == 2:
        inline_keyboard = InlineKeyboardMarkup()
        inline_keyboard.row(InlineKeyboardButton("Отмена", callback_data="cancel"),
                            InlineKeyboardButton("Добавить", callback_data="add"))

        sent_message = await message.answer(f"Вопрос и ответы:\n"
                             f"{user_data.get('question')}\n"
                             f"a) {user_data.get('true_answer')} - верный\n"
                             f"b) {user_data.get('false_answer_1')}\n"
                             f"c) {user_data.get('false_answer_2')}\n"
                             f"d) {message.text}", reply_markup=inline_keyboard)

        message_id = sent_message.message_id
        await state.update_data(message_id=message_id, false_answer_3=message.text)
        await state.set_state(StatesAdmin.add_question_choice_create_answers)
    elif false_answers_num == 1:
        await state.update_data(false_answers_num=false_answers_num + 1, false_answer_2=message.text)
        await message.answer("Введите третий неправильный ответ")
    elif false_answers_num == 0:
        await state.update_data(false_answers_num=false_answers_num + 1, false_answer_1=message.text)
        await message.answer("Введите второй неправильный ответ")



def register_commands(dp: Dispatcher):
    dp.register_message_handler(add_question_start, text="Добавить вопрос", state=StatesAdmin.admin)
    dp.register_callback_query_handler(choice_book,
                                       lambda c: c.data.startswith("book_"),
                                       state=StatesAdmin.add_question_choice)
    dp.register_callback_query_handler(choice_section_1,
                                       lambda c: c.data.startswith("section_"),
                                       state=StatesAdmin.add_question_choice)
    dp.register_callback_query_handler(choice_section_2,
                                       lambda c: c.data.startswith("subsection_"),
                                       state=StatesAdmin.add_question_choice)
    dp.register_callback_query_handler(choice_section_3,
                                       lambda c: c.data.startswith("sub_subsection_"),
                                       state=StatesAdmin.add_question_choice)
    dp.register_message_handler(add_question_name, state=StatesAdmin.add_question_name)
    dp.register_message_handler(add_question_true_answer, state=StatesAdmin.add_question_true_answer)
    dp.register_callback_query_handler(add_question_chatGPT,
                                       lambda c: c.data.startswith("chatGPT"),
                                       state=StatesAdmin.add_question_choice_create_answers)
    dp.register_callback_query_handler(add_question_add_in_database,
                                       lambda c: c.data.startswith("add"),
                                       state=StatesAdmin.add_question_choice_create_answers)
    dp.register_callback_query_handler(add_question_cancel,
                                       lambda c: c.data.startswith("cancel"),
                                       state=StatesAdmin.add_question_choice_create_answers)
    dp.register_callback_query_handler(add_question_himself,
                                       lambda c: c.data.startswith("himself"),
                                       state=StatesAdmin.add_question_choice_create_answers)
    dp.register_message_handler(add_question_false_answers, state=StatesAdmin.add_question_false_answer)
