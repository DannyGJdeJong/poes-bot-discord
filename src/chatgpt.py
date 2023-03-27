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
      model="gpt-3.5-turbo",
      messages=messages
    )

    return response









# def get_reply_from_chatgpt(user_id, input):
#   memory[user_id].append({"role": "user", "content": input})
#   messages = memory[user_id]
#   user_context = [{"role": "system", "content": context[user_id]}] if len(context[user_id]) > 0 else []
#   user_context = user_context + [{"role": "system", "content": 'You are able to use Discord\'s formatting system. This allows you to use **text** to make text bold and *text* to italize text. You will always start your response with your name in brackets followed by a relevant emoji. For example if your name is ChatGPT you will start chats with **[ChatGPT 😇]:** if your name is PoesGPT you will start chats with **[PoesGPT 🐾]:**'}]

#   try:
#     response = openai.ChatCompletion.create(
#       model="gpt-3.5-turbo",
#       messages=user_context + messages
#     )
#   except Exception as e:
#      return f"You have broken me :( {e}"

#   answer = response["choices"][0]["message"]["content"]

#   memory[user_id].append({"role": "assistant", "content": answer})

#   if len(memory[user_id]) > 6:
#      memory[user_id] = memory[user_id][-6:]

#   token_cost = response["usage"]["total_tokens"]

#   return (answer, token_cost)
