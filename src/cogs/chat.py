import discord
from discord.ext import commands
from discord.commands.context import ApplicationContext
from chatgpt import ChatGPTMessage, get_chatgpt_response

import state
import constants

class Chat(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.command(name="chat", description="Chat with ChatGPT")
    @discord.option("user", discord.User, description="The user's instance to chat with", required=False, default=None)
    async def chat(self, ctx: ApplicationContext, message: str, user: discord.User | None):
        await ctx.defer()

        # Default user to current user if not set
        if user is None:
            user = ctx.user

        # Retreive context and memory
        current_context = state.context[user.id]
        current_memory = state.memory[user.id]

        # Build message stack
        message: ChatGPTMessage = {"role": "user", "content": message}
        messages: list[ChatGPTMessage] = [{"role": "system", "content": current_context}] + current_memory + [message]

        # Get response from ChatGPT
        response = get_chatgpt_response(messages)
        response_message = response["choices"][0]["message"]

        # Append interaction to memory
        state.memory[user.id].append(message)
        state.memory[user.id].append(response_message)

        # Limit the memory
        state.memory[user.id] = state.memory[user.id][:-constants.MEMORY_SIZE]

        # Respond with the received message
        await ctx.followup.send(f"{response_message['content']}")
