from aiogram import types


async def check_age(message: types.Message):
    age = message.text
    try:
        age = int(age)
    except ValueError:
        await message.answer(text="Не правильный возраст")
        return False

    if age > 99:
        await message.answer(text="Не правильный возраст")
        return False

    return True
