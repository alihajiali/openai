from fastapi import APIRouter, HTTPException
import datetime, pytz, os, aiohttp
from openai import OpenAI
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
    client = OpenAI(
        api_key=os.getenv("OPENAI_API_KEY"),
        base_url=os.getenv("OPENAI_API_BASE"),
    )
    response = client.responses.create(
        model=data.model,
        input=data.message
    ).output[0].content[0].text
    await Chat.create(message=data.message, response=response, model=data.model)
    return response


@router.post("/gemini")
async def gemini(data:GeminiChatModel):
    async with aiohttp.ClientSession() as session:
        headers = {'Content-Type': 'application/json'}
        params = {'key': os.getenv("GEMINI_API_KEY")}
        json_data = {'contents': [{'parts': [{'text': data.message}]}]}
        response = (await (await session.post('https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent',params=params,headers=headers,json=json_data)).json())["candidates"][0]["content"]["parts"][0]["text"]
    await Chat.create(message=data.message, response=response, model="gemini")
    return response
