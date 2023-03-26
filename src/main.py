from collections import defaultdict
import discord
from discord import app_commands
import os
import openai

GUILD_ID = os.getenv("GUILD_ID")
DEFAULT_CONTEXT = os.getenv("DEFAULT_CONTEXT")

intents = discord.Intents.default()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

memory: defaultdict[str, list] = defaultdict(list)
context: defaultdict[str, str] = defaultdict(lambda: DEFAULT_CONTEXT)

def get_reply_from_chatgpt(user_id, input):
  memory[user_id].append({"role": "user", "content": input})
  messages = memory[user_id]
  user_context = [{"role": "system", "content": context[user_id]}] if len(context[user_id]) > 0 else []

  try:
    response = openai.ChatCompletion.create(
      model="gpt-3.5-turbo",
      messages=user_context + messages
    )
  except Exception as e:
     return f"You have broken me :( {e}"

  answer = response["choices"][0]["message"]["content"]

  memory[user_id].append({"role": "assistant", "content": answer})

  if len(memory[user_id]) > 6:
     memory[user_id] = memory[user_id][-6:]

  token_cost = response["usage"]["total_tokens"]

  return (answer, token_cost)

# Get context
@tree.command(name="getcontext", description="get a personalized context", guild=discord.Object(id=GUILD_ID))
async def resetcontext(interaction: discord.Interaction):
  await interaction.response.defer()

  await interaction.followup.send(f"Your context is: {context[interaction.user.id]}")

# Reset context
@tree.command(name="resetcontext", description="reset a personalized context to the default", guild=discord.Object(id=GUILD_ID))
async def resetcontext(interaction: discord.Interaction):
  await interaction.response.defer()

  context[interaction.user.id] = DEFAULT_CONTEXT

  await interaction.followup.send(f"Context reset succesfully")

# Clear context
@tree.command(name="clearcontext", description="clear a personalized context", guild=discord.Object(id=GUILD_ID))
async def clearcontext(interaction: discord.Interaction):
  await interaction.response.defer()

  context[interaction.user.id] = ""

  await interaction.followup.send(f"Context cleared succesfully")

# Set context
@tree.command(name="setcontext", description="set a personalized context", guild=discord.Object(id=GUILD_ID))
async def setcontext(interaction: discord.Interaction, contextinput: str):
  await interaction.response.defer()

  context[interaction.user.id] = contextinput

  await interaction.followup.send(f"Context set succesfully")

# Clear memory
@tree.command(name="clearmemory", description="clear the personalized memory", guild=discord.Object(id=GUILD_ID))
async def setcontext(interaction: discord.Interaction, contextinput: str):
  await interaction.response.defer()

  memory[interaction.user.id] = []

  await interaction.followup.send(f"Memory cleared succesfully")

# Chat
@tree.command(name="chat", description="chat with PoesGPT", guild=discord.Object(id=GUILD_ID))
async def chat(interaction: discord.Interaction, message: str):
  await interaction.response.defer()
  answer, token_cost = get_reply_from_chatgpt(interaction.user.id, message)

  # Unused ...
  money_cost = 0.002 / 1000 * token_cost

  # <@{interaction.user.id}>: {input} \n \n PoesGPT:
  await interaction.followup.send(f"{answer}")

@client.event
async def on_ready():
    await tree.sync(guild=discord.Object(id=GUILD_ID))

client.run(os.getenv("DISCORD_BOT_TOKEN"))
