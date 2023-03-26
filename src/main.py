from collections import defaultdict
import discord
from discord import app_commands
import os
import openai

GUILD_ID = os.getenv("GUILD_ID")

intents = discord.Intents.default()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

memory: defaultdict[str, list] = defaultdict(list)

def get_reply_from_chatgpt(user_id, input):
  memory[user_id].append({"role": "user", "content": input})
  messages = memory[user_id]

  try:
    response = openai.ChatCompletion.create(
      model="gpt-3.5-turbo",
      messages=messages
    )
  except Exception as e:
     return f"You have broken me :( {e}"

  answer = response["choices"][0]["message"]["content"]

  memory[user_id].append({"role": "assistant", "content": answer})

  if len(memory[user_id]) > 6:
     memory[user_id] = memory[user_id][-6:]

  token_cost = response["usage"]["total_tokens"]

  return (answer, token_cost)


@tree.command(name="chat", description="chat with PoesGPT", guild=discord.Object(id=GUILD_ID))
async def chat(interaction: discord.Interaction, input: str):
  await interaction.response.defer()
  answer, token_cost = get_reply_from_chatgpt(interaction.user.id, input)

  # Unused ...
  money_cost = 0.002 / 1000 * token_cost

  # <@{interaction.user.id}>: {input} \n \n PoesGPT:
  await interaction.followup.send(f"{answer}")

@client.event
async def on_ready():
    await tree.sync(guild=discord.Object(id=GUILD_ID))

client.run(os.getenv("DISCORD_BOT_TOKEN"))
