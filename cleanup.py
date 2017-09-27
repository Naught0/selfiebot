#!/bin/env python

import discord
from discord.ext import commands


class Cleanup:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='clean', aliases=['purge'])
    async def _clean(self, ctx, num_msg: int):
    # Check so that only my msgs are removed
    def check(message):
        return message.author.id == self.bot.user.id

    try:
        await ctx.channel.purge(check=check, limit=num_msg)
    except Exception as e:
        print(e)


def setup(bot):
    bot.add_cog(Cleanup(bot))
