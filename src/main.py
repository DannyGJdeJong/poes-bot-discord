import os
import discord
import constants

from cogs.context import Context
from cogs.chat import Chat
from cogs.memory import Memory

GUILD_ID = os.getenv("GUILD_ID")

bot = discord.Bot(debug_guilds=[constants.GUILD_ID])

@bot.event
async def on_ready():
    pass

bot.add_cog(Context(bot))
bot.add_cog(Chat(bot))
bot.add_cog(Memory(bot))
bot.run(constants.DISCORD_BOT_TOKEN)
