from fastapi import APIRouter, HTTPException
import datetime, pytz, openai, os
from typing import Literal
from ..schemas import ChatModel
from ..models import Chat

router = APIRouter(
    prefix="/v1/chat",
    tags=["CHAT"],
    responses={404: {"description": "Not found"}},
)

@router.post("")
async def main(data:ChatModel):
    openai.api_key = os.getenv("OPENAI_API_KEY")
    openai.api_base = os.getenv("OPENAI_API_BASE")
    response = openai.ChatCompletion.create(
        model=data.model,
        messages=[{"role": "user", "content": data.message}]
    )['choices'][0]['message']['content']
    await Chat.create(message=data.message, response=response, model=data.model)
    return response