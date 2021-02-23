import discord
import io
import contextlib
import textwrap
from traceback import format_exception
from discord.ext import commands
import asyncio
import datetime
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

class Eval(commands.Cog, command_attrs={"hidden": True}):
    def __init__(self, bot):
    	self.bot = bot
    
    class ErrorEmbed(discord.Embed):
        def __init__(self, description, **kwargs):
                         super().__init__(color=0x2F3136,
                         title="Uh..",
                         description=description,
                         timestamp=datetime.datetime.utcnow())
                         
    @commands.command(hidden=True,name="eval", aliases=["exec"], help="Evaluate code, idk.", brief="Evaluate code.")
    @commands.is_owner()
    async def _eval(self, ctx, *, code):
    	code = clean_code(code)
    	local_variables = {
    	"self": self,
    	"discord": discord,
    	"asyncio": asyncio,
    	"aiohttp": __import__('aiohttp'),
    	"sys": __import__('sys'),
    	"commands": commands,
    	"bot": self.bot,
    	"ctx.bot": self.bot,
    	"ctx": ctx,
    	"channel": ctx.channel,
    	"author": ctx.author,
    	"guild": ctx.guild,
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
    		await ctx.message.add_reaction(self.bot.emoji_dict["redTick"])
    		
    		
    	await ctx.message.add_reaction(self.bot.emoji_dict["greenTick"])
    	pager = Pag(
    	timeout=100,
    	entries=[result[i: i + 2000] for i in range(0, len(result), 2000)],
    	length=1,
    	prefix="```py\n",
    	suffix="```",
    	color = self.bot.grey
    	)
    	await pager.start(ctx)
    	
def setup(bot):
	bot.add_cog(Eval(bot))
