from discord.ext import commands
import discord
from typing import Union, Optional
import random

import datetime
from discord.ext import commands
from utils.PacBot import PacMe

class cooldown:
	def cooldown(self, seconds):
	       async def cooldown_predicate(ctx):

	           if not (cd := await ctx.bot.db.fetchrow(f'SELECT * FROM cooldown WHERE id={ctx.author.id} AND command=$1', str(ctx.command))):
	           	await ctx.bot.db.execute(f'INSERT INTO cooldown VALUES ({ctx.author.id}, $1, {int(time.time()+seconds)})', str(ctx.command))
	           	return True
	           else:
	           	ends_at = cd[0]['ends_at'] or 0
	           	if ends_at > time.time():
	           		raise commands.CommandOnCooldown(f'Command {ctx.command} is on cooldown', retry_after=ends_at - time.time())
	           	else:
	           	   await ctx.bot.db.execute(f'UPDATE cooldown SET ends_at={int(time.time()+seconds)} WHERE id={ctx.author.id} AND command=$1', str(ctx.command))
	           	   return True
	           return commands.check(cooldown_predicate)	

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
	
	@commands.command()
	@cooldown.cooldown(cooldown, 20)
	async def beg(self, ctx):
		money = random.randint(1, 201)
		try:
			data = await self.bot.db.fetchrow("SELECT * FROM economy WHERE user_id = $1", ctx.author.id)
			
			wallet = data['wallet']
			bank = data['bank']
			
			await ctx.embed(description=f"You earned **${money}**!")
			await self.bot.db.execute(f"UPDATE economy SET wallet = $1 WHERE user_id = $2", wallet + money, ctx.author.id)
		except Exception as e:
			print(e)
			raise self.bot.custom_errors.NotInDB("Your ID")					


def setup(bot):
	bot.add_cog(Economy(bot))									
