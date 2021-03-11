import discord
from discord.ext import commands
import asyncio
from utils.paginator import Paginator 



class Pag(Paginator):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
  

class Fun(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
	
	def get_pages(self):
	   	pages = []
	   	# Generate a list of 5 embeds
	   	for i in range(1, 6):
	   	   embed = discord.Embed()
	   	   embed.title = f"I'm the embed {i}!"
	   	   pages.append(embed)
	   	return pages

	
	@commands.command()
	@commands.is_owner()
	async def pag(self, ctx):
		pag = Paginator(pages=self.get_pages())
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
			msg.add_reaction("🍪")
			reaction, user = await self.bot.wait_for("reaction_add", timeout=20.0, check=check)
			if str(reaction.emoji) == "🍪":
				end = time.perf_counter()
				embed = discord.Embed(title=user, description=f"This fool took {round(end-start *1000, 2)}")
				await msg.edit(embed=embed)							
		except asyncio.TimeoutError:
			return
			
def setup(bot):
	bot.add_cog(Fun(bot))			