import platform
import discord
from discord.ext import commands
from collections import OrderedDict, deque, Counter
import psutil
import asyncio
import time
import os
import humanize
import datetime

class Bot(commands.Cog):
	
	def __init__(self, bot):
		self.bot = bot
		
	@commands.command(help="Get the latency of the bot.")
	async def ping(self, ctx):
		time_1 = time.perf_counter()
		await ctx.trigger_typing()
		time_2 = time.perf_counter()
		ping = round((time_2-time_1)*1000)	
		msgg = await ctx.send("Ping!")
		embed = discord.Embed(color=discord.Color.from_rgb(64, 64, 64), title="Pong!", description=f"Websocket Latency: ```{round(self.bot.latency * 1000, 2)}ms```\nTyping Latency: ```{ping}ms```")
		await msgg.edit(embed=embed)	
	
	@commands.command(help="Info about the bot.", aliases=['about'])
	async def Info(self, ctx):
	       x = await self.bot.fetch_user(784122061219954708)
	       process = psutil.Process(os.getpid())
	       embed = discord.Embed(color = discord.Color.from_rgb(64, 64, 64), title=f'{ctx.command.name}', description=f'{ctx.bot.description}\nNote: My prefix is **"{ctx.prefix}"**')
	       embed.add_field(name='Info:', value=f'<:member_join:596576726163914752> **Developer\'s -** [FrostiiWeeb](https://discord.com/users/746807014658801704), [Cyrus](https://discord.com/users/668906205799907348)\n<:member_join:596576726163914752> **Library -** [discord.py](https://pypi.org/project/discord.py/)\n<:member_join:596576726163914752> **Created - ** {humanize.naturaltime(x.created_at)}\n<:member_join:596576726163914752> **Command Credit -** **Rainbow#8292**, **averwhy#3899**, **Vaskel#5683**', inline=False)
	       embed.add_field(name='Stats:', value=f'<:member_join:596576726163914752> **Number of commands -** {len(self.bot.commands)}\n<:member_join:596576726163914752> **Guilds -** {len(list(map(str, [p.id for p in self.bot.guilds])))}\n<:member_join:596576726163914752> **Users -** {len(list(map(str, [p.id for p in self.bot.users])))}\n<:member_join:596576726163914752> **Using {humanize.naturalsize(process.memory_info().rss)} physical memory, {humanize.naturalsize(process.memory_info().vms)} virtual memory**', inline=False)
	       embed.add_field(name='Links:', value=f'<:member_join:596576726163914752> **Invite Link -** [Here](https://top.gg/bot/784122061219954708)\n<:member_join:596576726163914752> **Github -** [Here](https://github.com/FrostiiWeeb/PacMeSource)', inline=False)
	       await ctx.send(embed=embed)
	
	@commands.command(help="The invite of the bot.",aliases=['inv'])
	async def invite(self, ctx):
		emned = discord.Embed(title="```Invite URL:```", description="[Click Here](https://discord.com/api/oauth2/authorize?client_id=784122061219954708&permissions=2117730294&scope=bot)", colour=discord.Colour.from_rgb(64, 64, 64))
		await ctx.send(embed=emned)
	
	@commands.command(help="Get the source for the bot.", aliases=["src"])
	async def source(self, ctx):
	       embed = discord.Embed(
	       title="Heres the source!",
	       description="[Here!](https://github.com/FrostiiWeeb/PacMeSource/)",
	       colour=discord.Colour.blurple()
	       )
	       embed.add_field(name="Leave a star, if u use my code!", value="Enjoy!")
	       await ctx.send(embed=embed)
	@commands.command(help="The bot changelog.", aliases=['cl'])
	async def changelog(self, ctx):
	           embed = discord.Embed(
	           title="**Changelog:**",
	           description="```Re-added custom prefixes.```",
	           colour=self.bot.colour
	           )
	           await ctx.send(embed=embed)
	           
		
def setup(bot):
	bot.add_cog(Bot(bot))
