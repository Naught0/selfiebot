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

@commands.command(name='eval', hidden=True)
async def shell_access(self, ctx, *, cmd):
    """ Lets me access the VPS command line via the bot """
    process = await asyncio.create_subprocess_shell(cmd, stdout=asyncio.subprocess.PIPE)
    stdout, stderr = await process.communicate()
    try:
        if stdout:
            await ctx.send(f'`{cmd}`\n```{stdout.decode().strip()}```\n```{stderr.decode().strip()}')
        else:
            await ctx.send(f'`{cmd}` produced no output')

    except Exception as e:
        await ctx.send(f'Unable to send output\n```py\n{e}```')


# Get user token
with open('apikeys.json') as f:
	token = json.load(f)['selfbot']

bot.run(token, bot=False)