from discord.ext import commands
import discord
from typing import Union

class Economy(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		
	@commands.command(aliases=['bal'])
	async def balance(self, ctx, user : Union[discord.Member, int] = None):
		user = user or ctx.author
		
		try:
			data = await self.bot.db.fetchrow("SELECT * FROM economy WHERE user_id = $1", user.id)
			
			wallet = data['wallet']
			bank = data['bank']
			
			await ctx.embed(title=f"{user.name}'s balance", description=f"{self.bot.emoji_dict['greyTick']} Wallet: **${wallet}**\n{self.bot.emoji_dict['greyTick']} Bank: **${bank}**")
		except:
			raise self.bot.custom_errors.NotInDB("Your ID")


def setup(bot):
	bot.add_cog(Economy(bot))									
