from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.dispatcher import FSMContext
import asyncio
from time import sleep

api = ''
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())
kb = ReplyKeyboardMarkup(resize_keyboard=True)

class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()


button = KeyboardButton(text='Расчитать',)
button2 = KeyboardButton(text="Информация")

kb.row(button, button2)


@dp.message_handler(commands=['start'])
async def start_message(message):
    await message.answer("Привет! Я бот помогающий твоему здоровью."
                         " Нажмите 'Расчитать' для определения Вашей суточной нормы калорий", reply_markup=kb)


@dp.message_handler(text='Расчитать')
async def set_age(message):
    await message.answer("Введите свой возраст")
    await UserState.age.set()


@dp.message_handler(state=UserState.age)
async def set_growth(message, state):
    await state.update_data(age=message.text)
    # data = await state.get_data()
    await message.answer("Введите свой рост")
    await UserState.growth.set()


@dp.message_handler(state=UserState.growth)
async def set_weight(message, state):
    await state.update_data(growth=message.text)
    # data = await state.get_data()
    await message.answer("Введите свой вес")
    await UserState.weight.set()


@dp.message_handler(state=UserState.weight)
async def send_calories(message, state):
    await state.update_data(weight=message.text)
    data = await state.get_data()
    print(data)
    await message.answer("Запускаем калькулятор, пожалуйста ожидайте")
    sleep(5)
    calories = (10*float(data['weight']))+(6.25*float(data['growth']))-(5*float(data['age']))-161
    await message.answer(f'Ваша суточная норма калорий:{calories}. Приятного аппетита=)')
    await state.finish()


@dp.message_handler()
async def all_messages(message):
    await message.answer("Введите команду /start, чтобы начать общение")


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
