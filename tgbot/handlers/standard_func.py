from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import ContentTypes

from tgbot.handlers.buttons import show_button
from tgbot.utiles.database.firebase import check_admins_id
from tgbot.states.user_states import StatesAdmin


async def start(message: types.Message, state: FSMContext):
    await message.reply("Привет я бот для админов LotBook. Я помогу добавить новую книгу в базу данных, а также "
                        "создать новые вопросы к разделам книги и также сохранить их в БД.")
    print(message.from_user.id)
    if await check_admins_id(message.from_user.id):
        await state.set_state(StatesAdmin.admin)
        sent_message = await message.answer("Выберите нужную команду",
                                            reply_markup=show_button(["Добавить книгу", "Добавить вопрос"]))
        message_id = sent_message.message_id
        await state.update_data(message_id=message_id)
    else:
        await state.set_state(StatesAdmin.unknown_user)
        await message.answer("Извините, но вас нет в базе. Обратитесь к другим администраторам, "
                             "чтобы вас добавили.")


async def message_for_unknown_user(message: types.Message, state: FSMContext):
    if await check_admins_id(message.from_user.id):
        await state.set_state(StatesAdmin.admin)
        sent_message = await message.answer("Выберите нужную команду",
                                            reply_markup=show_button(["Добавить книгу", "Добавить вопрос"]))
        message_id = sent_message.message_id
        await state.update_data(message_id=message_id)
    else:
        await state.set_state(StatesAdmin.unknown_user)
        await message.answer("Извините, но вас нет в базе. Обратитесь к другим администраторам, "
                             "чтобы вас добавили.")


def register_commands(dp: Dispatcher):
    dp.register_message_handler(start, commands='start')
    dp.register_message_handler(message_for_unknown_user,
                                content_types=ContentTypes.TEXT,
                                state=StatesAdmin.unknown_user)
