from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardRemove
from dotenv import get_variables

from keyboards import contact_keyboard, gender_keyboard

config = get_variables(".env")

bot = Bot(token=config.get('TOKEN'))
dp = Dispatcher(bot, storage=MemoryStorage())
dp.middleware.setup(LoggingMiddleware())


class RegistrationForm(StatesGroup):
    waiting_for_contact = State()
    waiting_for_gender = State()
    waiting_for_age = State()


@dp.message_handler(commands=['start'])
async def start_bot(message: types.Message):
    await RegistrationForm.waiting_for_contact.set()
    await message.answer(text='Салам алейкум')
    await message.answer(text='Напишите свой номер телефона', reply_markup=contact_keyboard)


@dp.message_handler(content_types=types.ContentType.CONTACT, state=RegistrationForm.waiting_for_contact)
async def handle_contact(message: types.Message, state: FSMContext):
    contact = message.contact
    await state.update_data(contact=contact)
    await RegistrationForm.next()
    await message.answer(text='Выберите свой пол', reply_markup=gender_keyboard)


@dp.message_handler(lambda message: message.text.lower() == 'мужской' or message.text.lower() == 'женский',
                    state=RegistrationForm.waiting_for_gender)
async def handle_gender(message: types.Message, state: FSMContext):
    gender = message.text.lower()
    await state.update_data(gender=gender)
    await RegistrationForm.next()
    await message.answer(text='Сколько вам лет?', reply_markup=ReplyKeyboardRemove())


@dp.message_handler(lambda message: message.text.isdigit(), state=RegistrationForm.waiting_for_age)
async def handle_age(message: types.Message, state: FSMContext):
    age = int(message.text)
    await state.update_data(age=age)

    user_data = await state.get_data()

    await state.finish()

    await message.answer(text=f'Регистрация завершена. Ваш возраст: {age}.')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=False)
