import os
import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
intents = discord.Intents.default()
intents.message_content = True  # Enable the message content intent

bot = commands.Bot(command_prefix=os.getenv('COMMAND_PREFIX'), intents=intents)

@bot.command()
async def hello(ctx):
    await ctx.send('')

bot.run(os.getenv('DISCORD_TOKEN'))

