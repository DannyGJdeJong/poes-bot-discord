import discord
from discord.ext import commands
from discord.commands import SlashCommandGroup
from discord.commands.context import ApplicationContext

import state
import constants

class Context(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    context_group = SlashCommandGroup("context", "Modify context")

    @context_group.command(name="get", description="Get the current context")
    @discord.option("user", discord.User, description="The user to return the context for", required=False, default=None)
    async def get_context(self, ctx: ApplicationContext, user: discord.User | None):
        await ctx.defer()

        if user is None:
            user = ctx.user

        current_context = state.context[user.id]

        await ctx.followup.send(f"The context in use by <@{user.id}> is as follows: ```{current_context}```")

    @context_group.command(name="set", description="Set the context")
    @discord.option("wipe", bool, description="Whether to also clear memory", required=False, default=True)
    async def set_context(self, ctx: ApplicationContext, context: str, wipe: bool):
        await ctx.defer()

        state.context[ctx.user.id] = context

        if wipe:
            state.memory[ctx.user.id] = []

        await ctx.followup.send(f"Succesfully{' wiped memory and ' if wipe else ' '}set context to: ```{context}```")

    @context_group.command(name="reset", description="Reset the context to the default")
    @discord.option("wipe", bool, description="Whether to also clear memory", required=False, default=True)
    async def reset_context(self, ctx: ApplicationContext, wipe: bool):
        await ctx.defer()

        state.context[ctx.user.id] = constants.DEFAULT_CONTEXT

        if wipe:
            state.memory[ctx.user.id] = []

        await ctx.followup.send(f"Succesfully{' wiped memory and ' if wipe else ' '}reset context to: ```{constants.DEFAULT_CONTEXT}```")

    @context_group.command(name="clear", description="Clear the context")
    @discord.option("wipe", bool, description="Whether to also clear memory", required=False, default=True)
    async def clear_context(self, ctx: ApplicationContext, wipe: bool):
        await ctx.defer()

        state.context[ctx.user.id] = ""

        if wipe:
            state.memory[ctx.user.id] = []

        await ctx.followup.send(f"Succesfully{' wiped memory and ' if wipe else ' '}cleared context")
