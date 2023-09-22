import asyncio
import openai

from tgbot.utiles.secretData.config import config


openai.api_key = f"{config.OPENAI_API_KEY}"


async def create_chat_completion():
    """
    В messages мы можем составить диалог и указать поведение ассистента, на которое он будет ориентироваться
    для последующих своих ответах. Ответ приходит в json формате, откуда далее мы вытаскиваем ответ.
    :return:
    """
    chat_completion_resp = await openai.ChatCompletion.acreate(
                model="gpt-4",
                messages=[
                {"role": "system", "content": "Ты должен составлять вопросы и ответы для теста, указывая правильный ответ."
                                              "Вопросы должны быть составлены только по материалу из указанной части главы "
                                              "в указанной книге. "},  # Задаем поведение помощнику
                {"role": "user", "content": 'Напиши 4 вопроса с 4 вариантами ответов, указав правильный, только по '
                                            'материалу из части "Детские и юношеские годы '
                                            'Адольфа Титлера" главы - "Рождение Третьего Рейха"  в книге под названием '
                                            '"Взлёт и падение третьего рейха" автор - Уильем Ширер.'},  # Задаем вопрос боту

                ]
    )

    # response['choices'][0]['message']['content']

    print(chat_completion_resp.choices[0].message.content)

asyncio.run(create_chat_completion())



