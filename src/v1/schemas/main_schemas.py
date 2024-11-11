from pydantic import BaseModel, Field
from typing import Optional


class ChatModel(BaseModel):
    message:str=""
    model:str="gpt-4o-mini"


class GeminiChatModel(BaseModel):
    message:str=""
