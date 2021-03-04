import discord
from discord.ext import commands

class Config(commands.Cog, name="Config"):
	def __init__(self, bot):
		self.bot = bot
		
	@discord.ext.commands.command(aliases=['s'])
	async def settings(self, ctx):
		data = await self.bot.w.find(ctx.guild.id)
		
		if data:
			channel_id = data['channel_id']
			message = data['welcome_message']
			
			await ctx.embed(description=f"{self.bot.emoji_dict['greenTick']} Welcome:\nChannel_ID: {channel_id}\nWelcome_message: {message}")
		else:
			await ctx.embed(description=f"No settings.")
	
	@commands.command(usage="[prefix]")
	@commands.has_permissions(administrator=True)
	async def prefix(self, ctx, *, prefix="!*"):
	       """
	       Change the prefix!
	       """
	       # Insert the prefix into the database
	       await self.bot.config.upsert({"_id": ctx.guild.id, "prefix": prefix}) 
	       self.bot.cache[ctx.guild.id] = await self.bot.config.find(ctx.guild.id) # Set the cache.
	       await ctx.send(f"The guild prefix has been set to `{prefix}`. Use `{prefix}prefix [prefix]` to change it again!")


def setup(bot):
	bot.add_cog(Config(bot))