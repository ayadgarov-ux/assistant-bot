import asyncio
import os
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.client.telegram import TelegramAPIServer
from openai import OpenAI

BOT_TOKEN = os.environ.get("BOT_TOKEN")
PROXY_URL = "https://worker-purple-hill-b844.a-yadgarov.workers.dev"
OPENROUTER_KEY = os.environ.get("OPENROUTER_KEY")

client = OpenAI(
    api_key=OPENROUTER_KEY,
    base_url="https://openrouter.ai/api/v1"
)

session = AiohttpSession(api=TelegramAPIServer.from_base(PROXY_URL))
bot = Bot(token=BOT_TOKEN, session=session)
dp = Dispatcher()

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer(
        "Привет! Я твой ассистент.\n\n"
        "Команды:\n"
        "/search <вопрос> — поиск информации\n"
        "Любое сообщение — я отвечу через нейросеть."
    )

@dp.message(Command("search"))
async def cmd_search(message: types.Message):
    query = message.text.replace("/search", "").strip()
    if not query:
        await message.answer("Напиши вопрос после команды.")
        return
    
    await message.answer("Думаю...")
    
    try:
        response = client.chat.completions.create(
            model="openrouter/free",
            messages=[
                {"role": "system", "content": "Ты полезный ассистент. Отвечай кратко и по делу на русском языке."},
                {"role": "user", "content": query}
            ]
        )
        answer = response.choices[0].message.content
        await message.answer(answer)
    except Exception as e:
        await message.answer(f"Ошибка: {e}")

@dp.message()
async def echo(message: types.Message):
    try:
        response = client.chat.completions.create(
            model="openrouter/free",
            messages=[
                {"role": "system", "content": "Ты полезный ассистент. Отвечай кратко и по делу на русском языке."},
                {"role": "user", "content": message.text}
            ]
        )
        answer = response.choices[0].message.content
        await message.answer(answer)
    except Exception as e:
        await message.answer(f"Ошибка: {e}")

async def main():
    print("Бот запущен...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())    
# trigger redeploy
