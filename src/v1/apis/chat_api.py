from fastapi import APIRouter, HTTPException
import datetime, pytz, openai, os
from typing import Literal
from ..schemas import *
from ..models import Chat
import requests

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


@router.post("/gemini")
async def gemini(data:GeminiChatModel):
    headers = {'Content-Type': 'application/json'}
    params = {'key': 'AIzaSyBRcAVfNZJZcSuOLndUyXEbuWC6_QYMFe8'}
    json_data = {'contents': [{'parts': [{'text': data.message}]}]}
    return requests.post('https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent',params=params,headers=headers,json=json_data).json()["candidates"][0]["content"]["parts"][0]["text"]
