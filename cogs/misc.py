import discord
from discord.ext import commands
import platform
import time

class Misc(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
	

		
	async def get_github_sha(self):
		async with self.bot.session.get('https://api.github.com/repos/FrostiiWeeb/PacMe/commits') as f:
			resp = await f.json()

		sha = f"\`[{resp[0]['sha'][:6]}]({resp[0]['html_url']})\`\: {resp[1]['commit']['message']}\n\`[{resp[2]['sha'][:6]}]({resp[2]['html_url']})\`\: {resp[2]['commit']['message']}\n\`[{resp[3]['sha'][:6]}]({resp[3]['html_url']})\`\: {resp[3]['commit']['message']}\n\`[{resp[4]['sha'][:6]}]({resp[4]['html_url']})\`\: {resp[4]['commit']['message']}\n\`[{resp[5]['sha'][:6]}]({resp[5]['html_url']})\`\: {resp[5]['commit']['message']}"
		return sha
		
		
	async def get_github_url(self):
		async with self.bot.session.get('https://api.github.com/repos/FrostiiWeeb/PacMe/commits') as f:
			resp = await f.json()
		sha = resp[0]['commit']['tree']['sha']
		sha = sha[:-30]
		return sha		
		
	@commands.command(aliases=['botinfo', 'info'])
	async def about(self, ctx):
		"""
		Bot info.
		"""
		async with self.bot.session.get('https://api.github.com/repos/FrostiiWeeb/PacMe/commits') as f:
		          resp = await f.json()
		          await ctx.embed(description="**Github:**" + "\n" + "\n".join(
f"[`{commit['sha'][:6]}`]({commit['html_url']}) {commit['commit']['message']}" for commit in resp[:5]) + "\n" + f"**Info:**\n{self.bot.emoji_dict['dpy']} Library: [discord.py](https://pypi.org/project/discord.py)\n<:python:596577462335307777> Python Version: {__import__('platform').python_version()}")		
		
	@commands.command(aliases=['p'])
	async def ping(self, ctx):
		dbs = time.perf_counter()
		await self.bot.db.execute("SELECT 1 FROM prefixes")
		dbe = time.perf_counter()
		db = round((dbe - dbs) * 1000, 2)
		await ctx.embed(description=f"<:pg:818078755536502814> | **Database:**\n{db}ms")
	
	@commands.command()
	async def suggest(self, ctx):
		"""
		Suggest something!
		"""
		
		u = await self.bot.fetch_user(746807014658801704)
		
		await ctx.embed(description="Send an feature you want!")
		
		try:
			s = await self.bot.wait_for("message", timeout=30.0, check=lambda m: m.author == ctx.author and m.channel == ctx.channel)
			ss = s.content
			await ctx.embed(description="Alright! im sending that to my developer\'s!")
			embed = discord.Embed(color=self.bot.embed_color, title="New Feature Suggestion:", description=f"\"{ss}\"")
			msgg = await u.send(embed=embed)
			await msgg.add_reaction(self.bot.emoji_dict['greenTick'])
			await msgg.add_reaction(self.bot.emoji_dict['redTick'])			
			def check(reaction, user):
				return user.id in self.bot.owner_ids
			reaction, user = await self.bot.wait_for("reaction_add", check=check)
			if str(reaction.emoji) == self.bot.emoji_dict['greenTick']:
				def chec_k(m):
					return m.author.id in self.bot.owner_ids
				msg = await self.bot.wait_for("message", timeout=100.0, check=chec_k)				
				await ctx.author.send(embed=discord.Embed(color=self.bot.embed_color, title=f"{self.bot.emoji_dict['greenTick']} FrostiiWeeb#0400", description=msg.content))
			if str(reaction.emoji) == self.bot.emoji_dict['redTick']:
				def chec_k(m):
					return m.author.id in self.bot.owner_ids
				msg = await self.bot.wait_for("message", timeout=100.0, check=chec_k)				
				await ctx.author.send(embed=discord.Embed(color=self.bot.embed_color, title=f"{self.bot.emoji_dict['redTick']} FrostiiWeeb#0400", description=msg.content))				
		except Exception as e:
			print(e)	
		
		
def setup(bot):
	bot.add_cog(Misc(bot))