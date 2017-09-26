import discord
import asyncpg
import aiohttp
from datetime import datetime
from discord.ext import commands


bot = commands.Bot(command_prefix="?>", self_bot=True)

# For internet fun
bot.aio_session = aiohttp.ClientSession

# Create connection to postgresql server using pools
async def create_db_pool():
    with open('data/apikeys.json') as f:
        pg_pw = json.load(f)['postgres']
    bot.pg_con = await asyncpg.create_pool(user='james', password=pg_pw, database='discord_testing')
bot.loop.run_until_complete(create_db_pool())

@bot.event
async def on_ready():
	print(f'Client logged in at {datetime.now()}')

bot.run("mfa.Kd6-eyiOy4gD8cXDpT1m-1t7wE69Vx-cavTm3KX5yKZSfFlP_6txvZaE6ql4Nuw3xQnGaR3m_uP6_S4oh5Y2", bot=False)