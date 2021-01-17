import io
import time
from datetime import datetime
import asyncio
import aiohttp
import discord
from discord.ext import commands


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

    @commands.command(help="Take a screemshot of a website",aliases=["ss"])
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
                    color=discord.Color.from_rgb(48, 162, 242)
                )
                embed.set_image(url="attachment://screenshot.png")
                embed.set_footer(text=f"```Image fetched in {ping} ms```")

                message = await ctx.send(file=file, embed=embed)
                await message.add_reaction('🚮')
                def check(reaction, user):
                	return user == ctx.author and str(reaction.emoji) in ['🚮']
                	
                while True:
                	try:
                		reaction, user = await self.bot.wait_for("reaction_add", timeout=60.0, check=check)
                		
                		if str(reaction.emoji) == '🚮':
                			await message.delete()
                			await ctx.send(f"{ctx.author} deleted the screenshot.")
                			return
                	except asyncio.TimeoutError:
                		if not message:
                			return
                		else:
                		    await message.delete()

    @commands.command(help="The uptime for the bot.",aliases=['ut'])
    async def uptime(self, ctx):
        delta_uptime = datetime.utcnow() - self.bot.launch_time
        hours, remainder = divmod(int(delta_uptime.total_seconds()), 3600)
        minutes, seconds = divmod(remainder, 60)
        days, hours = divmod(hours, 24)
        embed = discord.Embed(title="```Uptime:```", description=f"```\n{days}d, {hours}h, {minutes}m, {seconds}s\n```", colour= 0x979c9f)
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Developer(bot))
