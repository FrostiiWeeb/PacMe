from discord.ext import commands
import json

# Local code

from utils.PacBot import PacMe
import utils.json_loader

import asyncio
import io
import contextlib
from traceback import format_exception
import textwrap
import discord
from discord.ext.buttons import Paginator


class Pag(Paginator):
    async def teardown(self):
        try:
            await self.page.clear_reactions()
        except discord.HTTPException:
            pass


async def GetMessage(
    bot, ctx, contentOne="Default Message", contentTwo="\uFEFF", timeout=100
):
    """
    This function sends an embed containing the params and then waits for a message to return
    Params:
     - bot (commands.Bot object) :
     - ctx (context object) : Used for sending msgs n stuff
     - Optional Params:
        - contentOne (string) : Embed title
        - contentTwo (string) : Embed description
        - timeout (int) : Timeout for wait_for
    Returns:
     - msg.content (string) : If a message is detected, the content will be returned
    or
     - False (bool) : If a timeout occurs
    """
    embed = discord.Embed(title=f"{contentOne}", description=f"{contentTwo}",)
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


bot = PacMe(allowed_mentions=discord.AllowedMentions(users=True, roles=False, everyone=False, replied_user=False))

@bot.group(invoke_without_command=True, name="eval", aliases=["exec"])
@commands.is_owner()
async def _eval(ctx, *, code):
    code = clean_code(code)
    
    if bot._underscore:
        local_variables = {
            "discord": discord,
            "commands": commands,
            "_bot": bot,
            "_ctx": ctx,
            "_channel": ctx.channel,
            "_author": ctx.author,
            "_guild": ctx.guild,
            "_message": ctx.message
        }
    else:
        local_variables = {
            "discord": discord,
            "commands": commands,
            "bot": bot,
            "_ctx": ctx,
            "channel": ctx.channel,
            "author": ctx.author,
            "_guild": ctx.guild,
            "message": ctx.message
        }    	

    stdout = io.StringIO()

    try:
        with contextlib.redirect_stdout(stdout):
            exec(
                f"async def func():\n{textwrap.indent(code, '    ')}", local_variables,
            )

            obj = await local_variables["func"]()
            result = f"{stdout.getvalue()}\n-- {obj}\n"
    except Exception as e:
        result = "".join(format_exception(e, e, e.__traceback__))

    pager = Pag(
        timeout=100,
        entries=[result[i: i + 2000] for i in range(0, len(result), 2000)],
        length=1,
        prefix="```py\n",
        suffix="```"
    )

    await pager.start(ctx)
    
@_eval.command(name="_")
async def _under(ctx):
	if bot._underscore:
		bot._underscore = False
		return await ctx.send("Eval underscore is now off.")
	bot._underscore = True
	return await ctx.send("Eval underscore is now on.")

if __name__ == "__main__":
	bot.run(bot._token)