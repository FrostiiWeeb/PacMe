import io
import time
from datetime import datetime
import asyncio
import aiohttp
import discord
from discord.ext import commands
from discord.ext import menus


class MenuSource(menus.ListPageSource):
    """
    For pagination, we need an instance of `MenuPages` (or an instance of a subclass of `MenuPages`), which will paginate our data
    and a page source to handle the formatting of our data. There are many different page sources that `ext-menus` offers.
    For this example we will be using `ListPageSource` as it is the simplest one.
    """
    def __init__(self, data):
        super().__init__(data, per_page=2)
        # Here we initialize our page source class with the data that we will be paginating and the amount of data to show per page.

    async def format_page(self, menu, data):
        """
        This function will handle the formatting of our data. It takes two arguments:
        `menu` - The `MenuPages` instance which will be paginating the pages returned from this page source.
        `data` - The current data for the page. Since we set the `per_page` kwarg to 2, we are expecting `data` to be
        a list with 2 values in it. (if `per_page` is set to one `data` will be the data itself, not a list with one item in it.)
        """
        embed = discord.Embed(description="\n".join(item for item in data))  # here we are creating an embed using the data as our description.
        return embed  # returning the embed

class Developer(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        self.screenshot_api = (
            "https://image.thum.io/get/"
            "width/1920/crop/675/maxAge/1/noanimate/{url}"
        )


    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.__class__.__name__} Cog has been loaded\n-----")

    @commands.command(brief="Get a screenshot of a website!",help="Take a screemshot of a website",aliases=["ss"])
    @commands.is_owner()
    async def screenshot(self, ctx, url):
        api_url = self.screenshot_api.format(url=url)
        start = time.perf_counter()

        async with aiohttp.ClientSession() as cs:
            async with cs.get(api_url) as r:
                res = await r.read()
                end = time.perf_counter()
                ping = round((end - start) * 1000)
                file = discord.File(io.BytesIO(res), filename="screenshot.png")
                embed = discord.Embed(
                    title=f"```Screenshot of {url}```",

                )
                embed.set_image(url="attachment://screenshot.png")
                embed.set_footer(text=f"Image fetched in {ping} ms")

                message = await ctx.send(file=file, embed=embed)
                await message.add_reaction('🚮')
                def check(reaction, user):
                	return user == ctx.author and str(reaction.emoji) in ['🚮']
                	
                while True:
                	try:
                		reaction, user = await self.bot.wait_for("reaction_add", timeout=60.0, check=check)
                		
                		if str(reaction.emoji) == '🚮':
                			await message.delete()
                			othermsg = await ctx.send(f"{ctx.author} deleted the screenshot.")
                			await asyncio.sleep(5)
                			await othermsg.delete()
                			return
                	except asyncio.TimeoutError:
                		if not message:
                			return
                		elif message:
                		    await message.delete()

    @commands.command(brief="Bot uptime",help="The uptime for the bot.",aliases=['ut'])
    async def uptime(self, ctx):
    	await ctx.send(embed=discord.Embed(description=f"I've been up for: **{__import__('humanize').precisedelta(self.bot.start_time, suppress=['milliseconds'], format='%0.0f')}**"))



def setup(bot):
    bot.add_cog(Developer(bot))
