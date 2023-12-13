import json
from typing import List

from google.cloud.firestore import AsyncClient
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
                                    "questions").document("empty").set({})
                            else:
                                await firestore_client.collection("Books").document(info["title"]).collection(
                                    "section 1").document(str(i + 1) + " " + content_sheet[i][0]).collection(
                                    "section 2").document(str(j) + " " + content_sheet[i][j][0]).collection(
                                    "section 3").document(str(l) + " " + content_sheet[i][j][l][0]).collection(
                                    "questions").document("empty").set({})

                    else:
                        await firestore_client.collection("Books").document(info["title"]).collection(
                              "section 1").document(str(i + 1) + " " + content_sheet[i][0]).collection(
                              "section 2").document(str(j) + " " + content_sheet[i][j][0]).collection(
                              "questions").document("empty").set({})

            else:
                await firestore_client.collection("Books").document(info["title"]).collection(
                    "section 1").document(str(i + 1) + " " + content_sheet[i][0]).collection(
                    "questions").document("empty").set({})
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


async def get_all_sections_4_of_book(name, section_1: str, section_2: str, section_3: str) -> List:

    docs = firestore_client.collection("Books").document(name).collection("section 1").document(
        section_1).collection("section 2").document(section_2).collection("section 3").document(
        section_3).collection("section 4").stream()
    result = [doc.id async for doc in docs]

    if result:
        return result
    else:
        raise ErrorGetSectionData


async def set_question(book: str, question: str, answers: [], section_1: str, section_2: str = None, section_3: str = None) -> None:
    try:
        if section_3 is not None:
            docs = firestore_client.collection("Books").document(book).collection("section 1").document(
            section_1).collection("section 2").document(section_2).collection("section 3").document(section_3).collection(
                "questions")

            try:
                await docs.document("empty").delete()
            except Exception:
                pass

            await docs.document(question).set({
                answers[0]: True, answers[1]: False, answers[2]: False, answers[3]: False
            })
        elif section_2 is not None:
            docs = firestore_client.collection("Books").document(book).collection("section 1").document(
            section_1).collection("section 2").document(section_2).collection("questions")

            try:
                await docs.document("empty").delete()
            except Exception:
                pass

            await docs.document(question).set({
                answers[0]: True, answers[1]: False, answers[2]: False, answers[3]: False
            })
        else:
            docs = firestore_client.collection("Books").document(book).collection("section 1").document(
                section_1).collection("questions")

            try:
                await docs.document("empty").delete()
            except Exception:
                pass

            await docs.document(question).set({
                answers[0]: True, answers[1]: False, answers[2]: False, answers[3]: False
            })
    except Exception as ex:
        print(ex)
        raise ErrorSendData


async def check_admins_id(user_id) -> bool:
    docs = await firestore_client.collection("Admins").document("telegram_id").get()
    if str(user_id) in docs.to_dict():
        return True
    else:
        return False


async def check_question_in_DB(question: str, book: str, section_1: str, section_2: str = None, section_3: str = None) -> bool:
    if section_3 is not None:
        docs = firestore_client.collection("Books").document(book).collection("section 1").document(
            section_1).collection("section 2").document(section_2).collection("section 3").document(
            section_3).collection("questions").stream()
        async for doc in docs:
            if doc.id == question:
                return doc.id == question

    elif section_2 is not None:
        docs = firestore_client.collection("Books").document(book).collection("section 1").document(
            section_1).collection("section 2").document(section_2).collection(
            "questions").document(question).stream()
        async for doc in docs:
            if doc.id == question:
                return doc.id == question
    else:
        docs = firestore_client.collection("Books").document(book).collection("section 1").document(
            section_1).collection("questions").stream()
        async for doc in docs:
            if doc.id == question:
                return doc.id == question
