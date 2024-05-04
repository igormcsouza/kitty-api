from fastapi import FastAPI
from mangum import Mangum
from pydantic import BaseModel

from api.chatbot import Chatbot, ChatbotException


app = FastAPI()

try:
    chatbot = Chatbot("models/")
except ChatbotException as e:
    raise Exception("Got error on chatbot loading.") from e


class CatBotBody(BaseModel):
    question: str


@app.post("/catbot")
async def catbot(body: CatBotBody):
    answer = await chatbot.get_response(body.question)

    return {"msg": answer}

handler = Mangum(app=app)
