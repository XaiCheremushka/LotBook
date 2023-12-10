import asyncio
# import openai
from openai import OpenAI

from tgbot.utiles.secretData.config import config

# openai.api_key = f"{config.OPENAI_API_KEY}"


client = OpenAI(
    api_key=config.OPENAI_API_KEY
)


async def create_answers(book: str, question: str, true_answer: str):
    """
    В messages мы можем составить диалог и указать поведение ассистента, на которое он будет ориентироваться
    для последующих своих ответах. Ответ приходит в json формате, откуда далее мы вытаскиваем ответ.
    :return:
    """
    response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    # Задаем поведение помощнику
                    {"role": "system", "content": "Пользователь тебе отправляет вопрос и правильный ответ к нему. "
                                              "А ты должен составить 3 неправильных ответа к нему по указанной книге."
                                              "Твой ответ должен выглядеть так: \nb) ответ\nc) ответ\nd) ответ"},
                    # Задаем вопрос боту
                    {"role": "user", "content": f'Составь 3 неправильных ответа к книге "{book}" по вопросу "{question}".'
                                                f'Правильный ответ: {true_answer}'},

                ]
    )

    # response['choices'][0]['message']['content']

    # print(chat_completion_resp.choices[0].message.content)
    return response['choices'][0]['message']['content']

# asyncio.run(create_answers("Взлет и падение Третьего Рейха",
#                            "Когда было заключено Мюнхенское соглашение по оккупации немцами Судетской области?",
#                            "Соглашение датировано 29 сентября, хотя подписано было утром 30 сентября"))



