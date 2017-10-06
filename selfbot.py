import discord
import asyncpg
import aiohttp
import json
from datetime import datetime
from discord.ext import commands

class SelfieBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix="?>", self_bot=True)

        with open('apikeys.json') as f:
            self.api_keys = json.load(f)

        # Default exts
        self.default_ext = ('eval', 'pyval', 'cleanup', 'meme',)

        # Create connection to postgres DB
        self.loop.run_until_complete(self.create_db_pool())

    async def create_db_pool(self):
        # Create connection to postgresql server using pools
        self.pg_con = await asyncpg.create_pool(user='james', password=self.api_keys['postgres'], database='discord_testing')

    def run(self):
        super().run(self.api_keys['selfbot'], bot=False)

    async def on_ready(self):
        self.bot_start_time = datetime.now()
        self.bot_start_time_str = self.bot_start_time.strftime('%B %d %H:%M:%S')
        print(f'Client logged in at {self.bot_start_time}')

        for ext in self.default_ext:
            try:
                self.load_extension(ext)
            except Exception as e:
                print(f'Failed to load extension {ext}\n{e}')
