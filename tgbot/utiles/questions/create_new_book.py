import asyncio

from tgbot.utiles.database.firebase import create_book
from tgbot.utiles.questions.parsing import parse


async def create_new_book(url: str):
    """
    Функция create_new_book добавляет новую кингу в базу данных со всей информацией по книге, в
    том числе и оглавление.

    :param url: Url-адрес страницы с книгой на сайте www.Litres.ru

    return: Оглавление.
    """

    content_sheet, info = parse(url)
    try:
        await create_book(content_sheet, info)
        print("Данные успешно отправлены")
    except Exception as ex:
        print("Ошибка отправки данных в БД")
        print(ex)



