from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ReplyKeyboardRemove
from dotenv import get_variables

from keyboards import contact_keyboard, gender_keyboard
from utils.checkIsAgeCorrect import check_age

config = get_variables(".env")

bot = Bot(token=config.get('TOKEN'))

dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def start_bot(message: types.Message):
    await message.answer(text='Салам алейкум')
    await message.answer(text='Напишите свой номер телефона', reply_markup=contact_keyboard)


@dp.message_handler(content_types=types.ContentType.CONTACT)
async def handle_contact(message: types.Message):
    contact = message.contact
    user_id = message.from_user.id
    phone_number = contact.phone_number
    first_name = contact.first_name
    last_name = contact.last_name
    await message.answer(text='Выберите свой пол', reply_markup=gender_keyboard)


@dp.message_handler(lambda message: message.text.lower() == 'мужской' or message.text.lower() == 'женский')
async def handle_age(message: types.Message):
    await message.answer(text='Сколько вам лет', reply_markup=ReplyKeyboardRemove())


@dp.message_handler(lambda message: message.text.lower() != 'мужской' or message.text.lower() != 'женский')
async def handle_gender_error(message: types.Message):
    await message.answer(text='Выберите один из двух вариантов', reply_markup=gender_keyboard)


@dp.message_handler(check_age)
async def handle_age(message: types.Message):
    await message.answer('Отлично')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=False)
