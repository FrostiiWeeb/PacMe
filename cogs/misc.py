import discord
from discord.ext import commands
import platform

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
		await ctx.embed(description=f"**Github:**\n{await self.get_github_sha()}\n**Info**:\n{self.bot.emoji_dict['dpy']} Library: [discord.py](https://pypi.org/project/discord.py)\n<:python:596577462335307777> Python version: {platform.python_version()}")
		
def setup(bot):
	bot.add_cog(Misc(bot))