from typing import Literal, TypedDict

import openai
import constants

openai.api_key = constants.OPENAI_API_KEY

class ChatGPTMessage(TypedDict):
    content: str
    role: Literal["user", "system", "assistant"]

class ChatGPTChoice(TypedDict):
    finish_reason: str
    index: int
    message: ChatGPTMessage

class ChatGPTUsage(TypedDict):
    completion_tokens: int
    prompt_tokens: int
    total_tokens: int

class ChatGPTResponse(TypedDict):
    choices: list[ChatGPTChoice]
    created: int
    id: str
    model: str
    object: str
    usage: ChatGPTUsage

def get_chatgpt_response(messages: list[ChatGPTMessage]) -> ChatGPTResponse:
    response: ChatGPTResponse = openai.ChatCompletion.create(
      model="gpt-4",
      messages=messages
    )

    return response
