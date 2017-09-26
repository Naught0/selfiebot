#!/bin/env python3
import discord
import asyncio
import eval_utils
from discord.ext import commands

class Eval:
    def __init__(self, bot):
        self.bot = bot
        self.pg_con = bot.pg_con

    @commands.command(name='eval', hidden=True)
    async def shell_access(self, ctx, *, cmd):
        """ Lets me access the VPS command line via the bot """
        cmd = eval_utils.cleanup_code(cmd)

        process = await asyncio.create_subprocess_shell(cmd, stdout=asyncio.subprocess.PIPE)
        stdout, stderr = await process.communicate()

        try:
            if stdout:
                await ctx.send(f'```{stdout.decode().strip()}```')
            elif stderr:
                await ctx.send(f'```{stderr.decode().strip()}```')
            else:
                await ctx.send(f'`{cmd}` produced no output')

        except Exception as e:
            await ctx.send(f'Unable to send output\n```py\n{e}```')

    @commands.group(invoke_without_command=True, name='sql', hidden=True)
    async def sql_execute(self, ctx, *, query):
        """ Lets me access the postgres database via discord """
        query = eval_utils.cleanup_code(query)

        try:
            res = await self.pg_con.execute(query)
        except Exception as e:
            return await ctx.send(f'```py\n{type(e).__name__}\n{str(e)}```')

        if not res:
            return await ctx.send(f'Sorry, `{query}` did not return anything.')

        await ctx.send(f'```sql\n{res}```')

    @sql_execute.command(name='fetch')
    async def sql_fetch(self, ctx, *, query):
        query = eval_utils.cleanup_code(query)

        try:
            res = await self.pg_con.fetch(query)
        except Exception as e:
            return await ctx.send(f'```py\n{type(e).__name__}\n{str(e)}```')

        if not res:
            return await ctx.send(f'Sorry, `{query}` did not return anything.')

        em = discord.Embed(color=discord.Color.dark_orange(), title='SQL Fetch')
        for k, v in res[0].items():
            em.add_field(name=k, value=v)

        await ctx.send(embed=em)


def setup(bot):
    bot.add_cog(Eval(bot))
