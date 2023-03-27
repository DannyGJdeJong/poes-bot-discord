import discord
from discord.ext import commands
from discord.commands import SlashCommandGroup
from discord.commands.context import ApplicationContext

import state

class Memory(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    memory_group = SlashCommandGroup("memory", "Modify memory")
    memory_clear_group = memory_group.create_subgroup("clear", "Clear memory")

    @memory_clear_group.command(name="all", description="Clear all messages from memory.")
    async def clear_all_memory(self, ctx: ApplicationContext):
        await ctx.defer()

        state.memory[ctx.author.id] = []

        await ctx.followup.send(f"Succesfully cleared memory")

    @memory_clear_group.command(name="last", description="Clear the last x messages from memory.")
    @discord.option("count", int, description="The amount of messages to clear", required=False, default=2)
    async def clear_last_memory(self, ctx: ApplicationContext, count: int):
        await ctx.defer()

        state.memory[ctx.author.id] = state.memory[ctx.author.id][:-count]

        await ctx.followup.send(f"Succesfully cleared last {count} messages from memory")
