import os
from dotenv import load_dotenv

load_dotenv()

GUILD_ID = os.getenv("GUILD_ID").split(",")
DEFAULT_CONTEXT = os.getenv("DEFAULT_CONTEXT")
DISCORD_BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
CHAT_GPT_MODEL = os.getenv("CHAT_GPT_MODEL")
MEMORY_SIZE = 8
