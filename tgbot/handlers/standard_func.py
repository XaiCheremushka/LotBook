from aiogram import types, Dispatcher


async def start(message: types.Message):
    await message.reply("Привет я бот, для проверки знаний по книгам.")



def register_commands(dp: Dispatcher):
    dp.register_message_handler(start, commands='start')
