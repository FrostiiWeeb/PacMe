import discord
from discord.ext import commands

class Config(commands.Cog, name="Config"):
	def __init__(self, bot):
		self.bot = bot
	
	@commands.Cog.listener()
	async def on_guild_join(self, guild):
	           await self.bot.db.execute(
	           "INSERT INTO prefixes(guild_id,prefix) VALUES($1,$2) ON CONFLICT (guild_id) DO UPDATE SET prefix = $2",
	           guild.id, "!*")
	           self.bot.cache.pop(guild.id, None)
	
	@commands.Cog.listener()
	async def on_guild_remove(self, guild):
	       await self.bot.db.execute("DELETE FROM prefixes WHERE guild_id = $1", guild.id)
	       self.bot.cache[guild.id] = "!*"
	       

		
	
	@commands.command(usage="[prefix]")
	@commands.has_permissions(administrator=True)
	async def prefix(self, ctx, *, prefix="!*"):
	       prefix = prefix.replace('\'', ' ')
	       """
	       Change the prefix!
	       """
	       # Insert the prefix into the database
	       await self.bot.db.execute("UPDATE prefixes SET prefix = $1 WHERE guild_id = $2", prefix, ctx.guild.id)
	       self.bot.cache[ctx.guild.id] = prefix
	       await ctx.embed(description=f"New prefix: **{prefix}**")


def setup(bot):
	bot.add_cog(Config(bot))