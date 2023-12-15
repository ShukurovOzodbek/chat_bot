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
    waiting_for_relation = State()
    waiting_for_message = State()


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


@dp.message_handler(state=RegistrationForm.waiting_for_gender)
async def handle_gender(message: types.Message, state: FSMContext):
    if message.text.lower() == 'мужской' or message.text.lower() == 'женский':
        gender = message.text.lower()
        await state.update_data(gender=gender)
        await RegistrationForm.next()
        await message.answer(text='Сколько вам лет?', reply_markup=ReplyKeyboardRemove())
    else:
        await message.answer(text='Напишите корректный пол или выберите', reply_markup=gender_keyboard)


@dp.message_handler(state=RegistrationForm.waiting_for_age)
async def handle_age(message: types.Message, state: FSMContext):
    try:
        age = int(message.text)
        if age > 99:
            await message.answer("Не допустимый возраст")
        else:
            await RegistrationForm.next()
            await state.update_data(age=age)
            await message.answer(text=f'Кому вы хотите сделать подарок.')
    except ValueError:
        await message.answer(text='Напишите корректный возраст')


@dp.message_handler(state=RegistrationForm.waiting_for_relation)
async def relation_handler(message: types.Message, state: FSMContext):
    await state.update_data(relation=message.text)
    await RegistrationForm.next()
    await message.answer(text='Опишите его интересы')


@dp.message_handler(state=RegistrationForm.waiting_for_message)
async def relation_handler(message: types.Message, state: FSMContext):
    await state.finish()
    user_data = await state.get_data()
    print(user_data)
    await message.answer(text='Подождите')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=False)
