import discord
import asyncpg
import aiohttp
import json
from datetime import datetime
from discord.ext import commands


bot = commands.Bot(command_prefix="?>", self_bot=True)

# For internet fun
bot.aio_session = aiohttp.ClientSession

# Create connection to postgresql server using pools
async def create_db_pool():
    with open('apikeys.json') as f:
        pg_pw = json.load(f)['postgres']
    bot.pg_con = await asyncpg.create_pool(user='james', password=pg_pw, database='discord_testing')
bot.loop.run_until_complete(create_db_pool())

@bot.event
async def on_ready():
    print(f'Client logged in at {datetime.now()}')

# Get user token
with open('apikeys.json') as f:
    token = json.load(f)['selfbot']

bot.default_ext = ('eval',)

if __name__ == "__main__":
    for ext in bot.default_ext:
        try:
            bot.load_extension(ext)
        except Exception as e:
            print(f'Failed to load extension {ext}\n{e}')

    bot.run(token, bot=False)