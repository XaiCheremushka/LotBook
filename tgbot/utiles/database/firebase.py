import asyncio
import json
from typing import List

from google.cloud.firestore import AsyncClient
# from google.cloud import firestore
from google.oauth2 import service_account

from tgbot.utiles.secretData.config import config
from tgbot.utiles.help_func.custom_exception import *


with open(fr"{config.PATH_FIREBASE_KEY}") as json_file:
    json_data = json.load(json_file)

firestore_client = AsyncClient(
    project=json_data['project_id'],
    credentials=service_account.Credentials.from_service_account_info(json_data),
)


async def create_book(content_sheet, info) -> None:
    """
    Функция create_book добавляет книгу в базу данных вместе с оглавлением.

    :param content_sheet: Двумерный список с оглавлением книги.
    :param info: Список с информацией по книге [название, ISBN, автор, количество страниц, дата выпуска].
    :return: None
    """
    try:
        await firestore_client.collection("Books").document(info["title"]).set({
            "ISBN": info["ISBN"], "autor": info["autor"], "total_pages": info["total_pages"], "date_of_publication": info["date_of_publication"]
        })

        for i in range(0, len(content_sheet)):
            await firestore_client.collection("Books").document(info["title"]).collection(
                    "section 1").document(str(i + 1) + " " + content_sheet[i][0]).set({})
            if isinstance(content_sheet[i], list) and len(content_sheet[i]) > 1:
                for j in range(1, len(content_sheet[i])):
                    await firestore_client.collection("Books").document(info["title"]).collection(
                              "section 1").document(str(i + 1) + " " + content_sheet[i][0]).collection(
                              "section 2").document(str(j) + " " + content_sheet[i][j][0]).set({})
                    if isinstance(content_sheet[i][j], list) and len(content_sheet[i][j]) > 1:
                        for l in range(1, len(content_sheet[i][j])):
                            await firestore_client.collection("Books").document(info["title"]).collection(
                                    "section 1").document(str(i + 1) + " " + content_sheet[i][0]).collection(
                                    "section 2").document(str(j) + " " + content_sheet[i][j][0]).collection(
                                    "section 3").document(str(l) + " " + content_sheet[i][j][l][0]).set({})
                            if isinstance(content_sheet[i][j][l], list) and len(content_sheet[i][j][l]) > 1:
                                # Можно увеличить дерево в будущем, дописав код здесь
                                await firestore_client.collection("Books").document(info["title"]).collection(
                                    "section 1").document(str(i + 1) + " " + content_sheet[i][0]).collection(
                                    "section 2").document(str(j) + " " + content_sheet[i][j][0]).collection(
                                    "section 3").document(str(l) + " " + content_sheet[i][j][l][0]).collection(
                                    "questions").document().set({})
                            else:
                                await firestore_client.collection("Books").document(info["title"]).collection(
                                    "section 1").document(str(i + 1) + " " + content_sheet[i][0]).collection(
                                    "section 2").document(str(j) + " " + content_sheet[i][j][0]).collection(
                                    "section 3").document(str(l) + " " + content_sheet[i][j][l][0]).collection(
                                    "questions").document().set({})

                    else:
                        await firestore_client.collection("Books").document(info["title"]).collection(
                              "section 1").document(str(i + 1) + " " + content_sheet[i][0]).collection(
                              "section 2").document(str(j) + " " + content_sheet[i][j][0]).collection(
                              "questions").document().set({})

            else:
                await firestore_client.collection("Books").document(info["title"]).collection(
                    "section 1").document(str(i + 1) + " " + content_sheet[i][0]).collection(
                    "questions").document().set({})
    except Exception as ex:
        print(ex)
        raise ErrorSendData


async def get_all_names_of_books() -> List:
    docs = firestore_client.collection("Books").stream()

    return [doc.id async for doc in docs]


async def get_all_sections_1_of_book(name: str) -> List:

    docs = firestore_client.collection("Books").document(name).collection("section 1").stream()
    result = [doc.id async for doc in docs]

    if result:
        return result
    else:
        raise ErrorGetSectionData


async def get_all_sections_2_of_book(name, section_1: str) -> List:
    docs = firestore_client.collection("Books").document(name).collection("section 1").document(
        section_1).collection("section 2").stream()
    result = [doc.id async for doc in docs]

    if result:
        return result
    else:
        raise ErrorGetSectionData


async def get_all_sections_3_of_book(name, section_1: str, section_2: str) -> List:

    docs = firestore_client.collection("Books").document(name).collection("section 1").document(
        section_1).collection("section 2").document(section_2).collection("section 3").stream()
    result = [doc.id async for doc in docs]

    if result:
        return result
    else:
        raise ErrorGetSectionData


async def set_question(name: str, question: str, answers: [], section_1: str, section_2: str = None, section_3: str = None) -> None:
    try:
        if section_3 is not None:
            await firestore_client.collection("Books").document(name).collection("section 1").document(
            section_1).collection("section 2").document(section_2).collection("section 3").document(section_3).collection(
                "questions").document(question).set({
                answers[0]: True, answers[1]: False, answers[2]: False, answers[3]: False
            })
        elif section_2 is not None:
            await firestore_client.collection("Books").document(name).collection("section 1").document(
            section_1).collection("section 2").document(section_2).collection(
                "questions").document(question).set({
                answers[0]: True, answers[1]: False, answers[2]: False, answers[3]: False
            })
        else:
            await firestore_client.collection("Books").document(name).collection("section 1").document(
                section_1).collection("section 2").document(section_2).collection(
                "questions").document(question).set({
                answers[0]: True, answers[1]: False, answers[2]: False, answers[3]: False
            })
    except Exception as ex:
        print(ex)
        raise ErrorSendData



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


