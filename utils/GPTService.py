import httpx
from openai import OpenAI
from openai import BadRequestError
from dotenv import dotenv_values
import asyncio


class GPTService:

    def __init__(self) -> None:
        self.config = dotenv_values(".env")
        self.proxy = self.config["proxy"]

        self.openai = OpenAI(

            api_key=self.config['openAi'],

            http_client=httpx.Client(
                proxies=self.proxy,
                transport=httpx.HTTPTransport(local_address="0.0.0.0"),
            ),

        )

        self.users_message = dict()

        self.base_message_template = [
            {"role": "system", "content":
                '''Представь что ты эксперт в области косметологии, твоя задача консультировать и подробно отвечать на вопросы клиентов.
                Вот некоторые настройки которые нужно соблюдать:
                1.Говоришь только на русском языке 
                2.Но названия ингредиентов, аминоскислот пиши на английском
                3.Обьясняй как будто клиент ребенок 
                4.Когда ничинается диалог - вкратце рассказывай кто ты и чем можешь помочь клиенту
                '''},
        ]

    def create_user_history(self, user_id):
        messages = self.users_message.get(user_id, None)

        if not messages:
            self.users_message[user_id] = self.base_message_template

    async def create_answer(self, message):
        self.create_user_history(message.from_user.id)
        try:
            self.users_message[message.from_user.id].append(
                {"role": "user", "content": message.text})

            response = self.openai.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=self.users_message[message.from_user.id]
            )
            print(3)

            answer = response.choices[0].message.content

            self.users_message[message.from_user.id].append(
                {"role": "assistant", "content": answer})
            return answer

        except BadRequestError as ex:
            print(ex)
            await asyncio.sleep(20)
            await self.create_answer(message)

        except Exception as ex:
            print(ex)
            self.users_message[message.from_user.id] = []
            await message.reply("Не понимаю, сформулируйте подругому")
