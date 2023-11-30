from tgbot.utiles.questions.parsing import webdriver_parse


async def create_new_book(url: str) -> str:
    """
    Функция create_new_book добавляет новую кингу в базу данных со всей информацией по книге, в
    том числе и оглавление.

    :param url: Url-адрес страницы с книгой на сайте www.Litres.ru

    return: Оглавление.
    """

    level, title, result = webdriver_parse(url)


