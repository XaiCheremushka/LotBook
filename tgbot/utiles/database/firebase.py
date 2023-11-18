# import firebase_admin
import json
from typing import List

# from firebase_admin import credentials

from google.cloud.firestore import AsyncClient
# from google.cloud import firestore
from google.oauth2 import service_account
from tgbot.utiles.secretData.config import config

# cred = credentials.Certificate("path/to/serviceAccountKey.json")
# firebase_admin.initialize_app(cred)

with open(fr"{config.PATH_FIREBASE_KEY}") as json_file:
    json_data = json.load(json_file)

firestore_client = AsyncClient(
    project=json_data['project_id'],
    credentials=service_account.Credentials.from_service_account_info(json_data),
)


async def create_book(list: List[List], info: List) -> None:
    """
    Функция create_book добавляет книгу в базу данных вместе с оглавлением.

    :param list: Двумерный список с оглавлением книги.
    :param info: Список с информацией по книге [название, ISBN, автор, количество страниц, дата выпуска].
    :return: None
    """

    await firestore_client.collection("Book").document(info[0]).set({
        "ISBN": info[1], "autor": info[2], "total_pages": info[3], "year_of_publication": info[4]
    })

    for i in range(0, len(list)):
        for j in range(0, len(list[i])):
            await firestore_client.collection("Book").document(info[0]).collection("sections").document(
                f"{i} {list[i][0]}").document(f"{j+1} {list[i][j]}")


async def get_table_of_content(book_name: str) -> List[List]:
    """
    Функция get_table_of_content возвращает оглавление указанной книги.

    :param book_name: Название книги.
    :param ISBN: ISBN.
    :return: Оглавление в виде двумерного массива.
    """
    docs = await firestore_client.collection("Book").document(book_name).collection("sections").stream()
    list = [[]]
    async for doc in docs:
        list[doc.id][doc.to_dict()]
    return docs.to_dict()


async def add_questions_to_book(book_name: str, questions: List[List], chapter: str = None) -> None:
    """
    Функция add_questions_to_book добавляет вопросы к указанной главе в книге.

    :param book_name: Название книги.
    :param questions: Вопросы с вариантами ответов к главе в виде двумерного массива ["вопрос"]["а","б","в","г"].
    :param chapter: Название главы.
    :return: None
    """
    # доделать
    # if chapter is None:
    #     for i in range(len())
    #     await firestore_client.collection("Book").document(book_name).collection("sections").document(
    #         f"{i} {list[i][0]}").document(f"{j} {list[i][j]}")
    # else:
    #     await firestore_client.collection("Book").document(book_name).collection("sections").document(
    #         f"{i} {list[i][0]}").document(f"{j} {list[i][j]}")