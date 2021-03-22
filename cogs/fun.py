import discord
from discord.ext import commands
import asyncio
from discord.ext.paginator import Paginator 
import time


class Pag(Paginator):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
  

class Fun(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	
	@commands.command()
	@commands.is_owner()
	async def cmdstats(self, ctx):
		embed1 = discord.Embed()
		for db in await self.bot.db.fetch("SELECT * FROM cmdstats"):
			name = db['command']
			usage = db['usage']			
			embed1.add_field(name=name, value=usage, inline=False)
		pag = Paginator(entries=[embed1])
		return await pag.start(ctx)
	
	@commands.command(aliases=['c'])
	async def cookie(self, ctx):
		"""
		Cookie command!
		"""
		def check(reaction, user):
			return str(reaction.emoji) == "🍪" and user != ctx.me
		try:
			start = time.perf_counter()
			msg = await ctx.send(embed=discord.Embed(title="Get the :cookie:!", description="Go!"))
			await msg.add_reaction("🍪")
			reaction, user = await self.bot.wait_for("reaction_add", timeout=20.0, check=check)
			if str(reaction.emoji) == "🍪":
				end = time.perf_counter()
				embed = discord.Embed(title=user.name, description=f"This fool took {round(end-start, 2)} seconds.")
				await msg.edit(embed=embed)							
		except asyncio.TimeoutError:
			return
			
def setup(bot):
	bot.add_cog(Fun(bot))			