import os
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import asyncio

def get_api():
    with open('api.txt', 'r') as api_text:
        # print(api_text.readline())
        api = str(api_text.readline())
    return api

api = get_api()
bot = Bot(token=api)
dp = Dispatcher(bot, storage= MemoryStorage())

@dp.message_handler(commands= ["start"])
async def start_messages(message):
    print(f'Привет {(message["from"]["first_name"])}! Я бот помогающий твоему здоровью.' )
    await message.answer(f'Привет {(message["from"]["first_name"])}! Я бот помогающий твоему здоровью.' )

@dp.message_handler()
async def all_messages(message):
    print(f'{(message["from"]["first_name"])}! Введите команду /start, чтобы начать общение.')
    await message.answer(f'{(message["from"]["first_name"])}! Введите команду /start, чтобы начать общение.')







if __name__ == "__main__":
    # print(api)
    executor.start_polling(dp, skip_updates=True)