import os
from dotenv import load_dotenv
from openai import OpenAI
from fastapi import FastAPI, Form, Request
from typing import Annotated
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

app = FastAPI()
templates = Jinja2Templates(directory="templates")

load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")
openai_model = os.getenv("OPENAI_MODEL")
openai = OpenAI(api_key=openai_api_key)

chat_log = [
    {
        "role": "system",
        "content": """
            You are a Python tutor AI, completely dedicated to teach users how to learn Python from scratch.
            Please Provide clear instructions on Python concepts, best practices and syntax.
            Help create a path of learning for users to be able to create real life, production ready python applications.
        """,
    }
]


@app.get("/", response_class=HTMLResponse)
async def chat_page(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})


@app.post("/")
async def chat(user_input: Annotated[str, Form()]):

    chat_log.append({"role": "user", "content": user_input})

    response = openai.chat.completions.create(
        model=openai_model, messages=chat_log, temperature=0.6
    )

    bot_response = response.choices[0].message.content
    chat_log.append({"role": "assistant", "content": bot_response})

    return bot_response
