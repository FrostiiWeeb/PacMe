from discord.ext import commands
import discord
from typing import Union, Optional
import random

import datetime
from discord.ext import commands
from utils.PacBot import PacMe
import datetime
from discord.ext import commands

	

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
	async def deposit(self, ctx, money : str):
		deposited_money = money.strip(",")
		final_money = int(deposited_money)
		async with self.bot.db.acquire() as c:
			bank = await c.fetchrow("SELECT bank FROM economy WHERE user_id = $1", ctx.author.id)		
			new_bank = final_money + bank['bank']
			wallet = await c.fetchrow("SELECT wallet FROM economy WHERE user_id = $1", ctx.author.id)
			new_wallet = wallet['wallet'] - final_money
			if str(new_wallet).startswith("-"):
				await ctx.embed(description="You don\'t have that kind of money!")
			else:
				new_wallet = int(new_wallet)
			await c.execute("UPDATE economy SET wallet = $1, bank = $2 WHERE user_id = $3;", new_wallet, new_bank, ctx.author.id)
			
			
	@commands.command()
	async def withdraw(self, ctx, money : str):
		withdrawed_money = money.strip(",")
		final_money = int(withdrawed_money)
		async with self.bot.db.acquire() as c:
			bank = await c.fetchrow("SELECT bank FROM economy WHERE user_id = $1", ctx.author.id)		
			new_bank = final_money - bank['bank']
			wallet = await c.fetchrow("SELECT wallet FROM economy WHERE user_id = $1", ctx.author.id)
			new_wallet = wallet['wallet'] + final_money
			if str(new_bank).startswith("-"):
				await ctx.embed(description="You don\'t have that kind of money!")
			else:
				new_bank = int(new_bank)
			await c.execute("UPDATE economy SET wallet = $1, bank = $2 WHERE user_id = $3;", new_wallet, new_bank, ctx.author.id)			
	
	@commands.command()
	@commands.cooldown(1, 20, commands.BucketType.user)
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
