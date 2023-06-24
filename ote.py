import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True  # Enable the message content intent

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.command()
async def hello(ctx):
    await ctx.send('Gay-Faggot')

bot.run('put token here')

