from dotenv import get_variables
from openai import OpenAI

config = get_variables(".env")

client = OpenAI(
    organization=config["ORGANIZATION"],
    api_key=config["GPT_KEY"]
)


def ask_gpt(prompt: str):
    stream = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        stream=True,
    )
    message = ""
    for chunk in stream:
        if chunk.choices[0].delta.content is not None:
            message += chunk.choices[0].delta.content

    return message



