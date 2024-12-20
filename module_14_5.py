from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

import module_14_3_db
from module_14_3_db import *

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
kb = ReplyKeyboardMarkup()
button_info = KeyboardButton(text="Информация")
button_calc = KeyboardButton(text="Рассчитать")
button_buy = KeyboardButton(text="Купить")
kb.resize_keyboard = True
kb.add(button_info)
kb.add(button_calc)
kb.add(button_buy)

kb_in = InlineKeyboardMarkup()
button_cal_in = InlineKeyboardButton(text='Рассчитать норму калорий', callback_data='calories')
button_for_in = InlineKeyboardButton(text='Формулы расчёта', callback_data='formulas')
kb_in.add(button_cal_in)
kb_in.add(button_for_in)

list_prod = module_14_3_db.db_read()

kb_prod = InlineKeyboardMarkup()
for i,j in zip(range(len(list_prod.values())), list_prod.values()):
    # print(i, j)
    exec ("button_p"+str(i+1)+ "= InlineKeyboardButton(text=j[0], callback_data='product_buying')")

kb_prod.add(button_p1)
kb_prod.add(button_p2)
kb_prod.add(button_p3)
kb_prod.add(button_p4)

@dp.message_handler(text = "Рассчитать")
async def main_menu(message):
    await message.answer('Выберите опцию:', reply_markup=kb_in)

@dp.callback_query_handler(text= "formulas")
async def get_formulas(call):
    await call.message.answer('Упрощенный вариант формулы Миффлина-Сан Жеора:\n для мужчин: 10 х вес (кг) + 6,25 x рост (см) – 5 х возраст (г) + 5;\nдля женщин: 10 x вес (кг) + 6,25 x рост (см) – 5 x возраст (г) – 161.\n')
    await call.answer()

@dp.callback_query_handler(text = "calories")
async def set_age(call):
    await call.message.answer('Введите свой возраст:')
    await UserState.age.set()
    await call.answer()

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
    await message.answer(f'Привет {(message["from"]["first_name"])}! Я бот помогающий твоему здоровью.', reply_markup = kb )

    # print(message)

@dp.message_handler(text='Купить')
async def get_buying_list(message):
    all_prod = module_14_3_db.db_read()
    for p in all_prod.values():
        with open(p[3],'rb') as img:
            await message.answer_photo(img, f"Название: {p[0]} | Описание: {p[1]} | Цена: {p[2]}")
    await message.answer("Выберите продукт для покупки:", reply_markup = kb_prod)
@dp.message_handler()
async def all_messages(message):
    # print(f'{(message["from"]["first_name"])}! Введите команду /start, чтобы начать общение.')
    await message.answer(f'{(message["from"]["first_name"])}! Введите команду /start, чтобы начать общение.')

@dp.callback_query_handler(text= "product_buying")
async def send_confirm_message(call):
    await call.message.answer('Вы успешно приобрели продукт!')
    await call.answer()





if __name__ == "__main__":
    # print(api)
    executor.start_polling(dp, skip_updates=True)