import os
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import asyncio
from aiogram.dispatcher.filters.state import State, StatesGroup

data = {}

class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()

def get_api():
    with open('api.txt', 'r') as api_text:
        # print(api_text.readline())
        api = str(api_text.readline())
    return api

api = get_api()
bot = Bot(token=api)
dp = Dispatcher(bot, storage= MemoryStorage())

@dp.message_handler(text = "Calories")
async def set_age(message):
    await message.answer('Введите свой возраст:')
    await UserState.age.set()

@dp.message_handler(state = UserState.age)
async def set_growth(message, state):
    await state.update_data(age = message.text)
    # print(await state.get_data())
    await message.answer(f"Введите свой рост:")
    await UserState.growth.set()

@dp.message_handler(state = UserState.growth)
async def set_weight(message, state):
    await state.update_data(growth = message.text)
    # print(await state.get_data())
    await message.answer(f"Введите свой вес:")
    await UserState.weight.set()

@dp.message_handler(state = UserState.weight)
async def send_calories(message, state):
    global data
    await state.update_data(weight = message.text)
    data = await state.get_data()
    # print(data)
    # для мужчин: 10 х вес (кг) + 6,25 x рост (см) – 5 х возраст (г) + 5
    calories = 10*int(data['weight'])+6.25*int(data['growth'])-5*int(data['age'])+5
    await message.answer(f"Результат: {calories}ккал")
    await state.finish()



@dp.message_handler(commands= ["start"])
async def start_messages(message):
    global data
    # print(f'Привет {(message["from"]["first_name"])}! Я бот помогающий твоему здоровью.' )
    await message.answer(f'Привет {(message["from"]["first_name"])}! Я бот помогающий твоему здоровью.' )
    # print(message)

@dp.message_handler()
async def all_messages(message):
    # print(f'{(message["from"]["first_name"])}! Введите команду /start, чтобы начать общение.')
    await message.answer(f'{(message["from"]["first_name"])}! Введите команду /start, чтобы начать общение.')







if __name__ == "__main__":
    # print(api)
    executor.start_polling(dp, skip_updates=True)