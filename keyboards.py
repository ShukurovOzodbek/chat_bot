from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

contact = KeyboardButton('Отправить свой контакт ☎️', request_contact=True)

contact_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
contact_keyboard.add(contact)

genders = ['Мужской', 'Женский']
gender_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
for gender in genders:
    keyboard = KeyboardButton(gender)
    gender_keyboard.add(keyboard)
