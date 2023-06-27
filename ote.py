import os
import asyncio
import logging

from discord.ext.commands import Bot
from discord import Intents
from dotenv import load_dotenv

class MyBot(Bot):

    def __init__(self):
        load_dotenv()
        self.command_prefix = os.getenv('COMMAND_PREFIX')
        super().__init__(command_prefix=self.command_prefix, intents=Intents.all())
        
    async def setup_hook(self):
        for file in (_ for _ in os.listdir("./cogs") if _.endswith('py') and not _.startswith('_')):
            print(file)
            await self.load_extension(f"cogs.{file.split('.')[0]}")

client = MyBot()
asyncio.run(client.start(os.getenv('DISCORD_TOKEN')))
