from aiogram.types import Message
from dotenv import get_variables
from openai import OpenAI

config = get_variables(".env")

client = OpenAI(
    organization=config["ORGANIZATION"],
    api_key=config["GPT_KEY"]
)


async def ask_gpt(message: Message, bot, to_gpt_text):
    answer = await message.answer(text="Подождите пожалуйста...")
    stream = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user",
                   "content": F'Я хочу сделать {to_gpt_text.get("who")} подарок на новый год. Его интересы {to_gpt_text.get("interests")}. '
                              F'Дай мне спосок подарков'}],
        stream=True,
    )

    text = ""
    for chunk in stream:
        if chunk.choices[0].delta.content is not None:
            text += chunk.choices[0].delta.content

    await message.answer(text=text)

    await bot.delete_message(chat_id=answer.chat.id, message_id=answer.message_id)
