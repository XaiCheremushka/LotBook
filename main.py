import logging

from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.utils.executor import start_webhook

from tgbot.handlers import start
from tgbot.utiles.questions.create_new_book import create_new_book
from tgbot.utiles.secretData.config import config


bot = Bot(token=config.BOT_TOKEN.get_secret_value())
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

WEBHOOK_HOST = config.WEBHOOK_HOST
WEBHOOK_PATH = f'/webhook/{config.BOT_TOKEN.get_secret_value()}'
WEBHOOK_URL = f'{WEBHOOK_HOST}{WEBHOOK_PATH}'

WEBAPP_HOST = config.WEBAPP_HOST
WEBAPP_PORT = config.WEBAPP_PORT



async def on_startup(dispatcher):
    await bot.set_webhook(WEBHOOK_URL, drop_pending_updates=True)
    start.register_commands(dispatcher)


async def on_shutdown(dispatcher):
    await bot.delete_webhook()


@dp.message_handler(commands=['admin'])
async def admin_panel(message: types.Message):
    await message.answer("Выберите нужную команду", reply_markup=show_button(["Добавить книгу", "Добавить вопрос"]))


@dp.message_handler(text=["Добавить книгу"])
@dp.message_handler(commands=['Добавить книгу'])
async def statisticUserBack(message: types.Message):
    url_Litres = "https://www.litres.ru/book/aleksey-georgievich/krasnye-partizany-na-vostoke-rossii-1918-1922-deviaci-69367450/"
    await message.answer('Подождите. Идёт создание книги в Базе Данных.')
    await create_new_book(url_Litres)
    await message.answer('Данные отправлены')


def show_button(list_menu):
    """Принимает список и превращает его в кнопки"""
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*list_menu)
    return keyboard


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    start_webhook(
        dispatcher=dp,
        webhook_path=WEBHOOK_PATH,
        skip_updates=False,
        on_startup=on_startup,
        on_shutdown=on_shutdown,
        host=WEBAPP_HOST,
        port=WEBAPP_PORT,
    )