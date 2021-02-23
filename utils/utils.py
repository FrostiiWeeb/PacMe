import discord
import inspect
from discord.ext import commands
import json
import contextlib
import textwrap
from traceback import format_exception
from discord.ext import commands
import asyncio
import datetime
from discord.ext.buttons import Paginator
from discord.ext import owoify

class Pag(Paginator):
    async def teardown(self):
        try:
            await self.page.clear_reactions()
        except discord.HTTPException:
            pass


async def GetMessage(
    bot, ctx, contentOne="Default Message", contentTwo="\uFEFF", timeout=100
):
    
    embed = discord.Embed(title=f"{contentOne}", description=f"{contentTwo}", color=bot.grey)
    sent = await ctx.send(embed=embed)
    try:
        msg = await bot.wait_for(
            "message",
            timeout=timeout,
            check=lambda message: message.author == ctx.author
            and message.channel == ctx.channel,
        )
        if msg:
            return msg.content
    except asyncio.TimeoutError:
        return False


def clean_code(content):
    if content.startswith("```") and content.endswith("```"):
        return "\n".join(content.split("\n")[1:])[:-3]
    else:
        return content


async def get_src(ctx, source):
   src = inspect.getsourcelines(source)
   pager = Pag(
   timeout=100,
   entries=[src[i: i + 2000] for i in range(0, len(src), 2000)],
   length=1,
   color = 0x2f3136
   )
   await pager.start(ctx)	

async def make_cog(file, cog_name):
		cog = f"import discord\nfrom discord.ext import commands\n\nclass {cog_name}(commands.Cog):\n    def __init__(self, bot):\n        self.bot = bot\n\n\ndef setup(bot):\n    bot.add_cog({cog_name}(bot))"
		f = open(file, 'w').write(cog)		

async def to_embed(ctx, **kwargs):
	await ctx.embed(**kwargs)							