import discord
from discord.ext import commands

bot = commands.Bot(command_prefix="?>", self_bot=True)

@bot.command()
async def add(ctx, left: int, right: int):
	await ctx.send(left + right)

bot.run("mfa.Kd6-eyiOy4gD8cXDpT1m-1t7wE69Vx-cavTm3KX5yKZSfFlP_6txvZaE6ql4Nuw3xQnGaR3m_uP6_S4oh5Y2", bot=False)