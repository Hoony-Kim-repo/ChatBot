from openai import OpenAI
import os
from dotenv import load_dotenv
from fastapi import FastAPI, Form

load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")
openai = OpenAI(api_key=openai_api_key)

chat_log = []

while True:
    user_input = input()

    if user_input.lower() == "stop":
        break

    chat_log.append({"role": "user", "content": user_input})

    response = openai.chat.completions.create(
        model="gpt-3.5-turbo", messages=chat_log, temperature=0.6
    )

    bot_response = response.choices[0].message.content
    chat_log.append({"role": "assistant", "content": bot_response})

    print(bot_response)
