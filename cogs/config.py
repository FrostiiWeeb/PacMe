import discord
from discord.ext import commands

class Config(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
	
	@commands.command()
	@commands.has_permissions(administrator=True)
	async def prefix(self, ctx, *, prefix="!*"):
	       await self.bot.config.upsert({"_id": ctx.guild.id, "prefix": prefix})
	       self.bot.cache[ctx.guild.id] = await self.bot.config.find(ctx.guild.id)        
	       await ctx.send(f"The guild prefix has been set to `{prefix}`. Use `{prefix}prefix [prefix]` to change it again!")


def setup(bot):
	bot.add_cog(Config(bot))