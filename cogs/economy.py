import discord
from discord.ext import commands
import random
from typing import Union

class Economy(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		self.amt = __import__('random').randint(1, 7)
		
	async def open_account(self, user):
		data = await self.get_bank_data(user)
		
		return data			
		
	async def get_bank_data(self, user):
		data = await self.bot.eco.find(user.id)
		
		if not data:
			await self.bot.eco.upsert({"_id": user.id, "wallet": 100, "bank": 0, "bankc": 500})
		else:
			return data			
	
	async def update_bal(self, user, wallet, bank, bankc):
		data = await self.open_account(user)
		
		if not data:
			await self.open_account(user)
		
		await self.bot.eco.upsert({"_id": user.id, "wallet": wallet, "bank": bank, "bankc": bankc})
	
	@commands.command(name="balance", aliases=["bal"], help="Get the balance of a user!")
	async def balance(self, ctx, user : Union[discord.Member, int] = None):
		
		user = user or ctx.author
		
		data = await self.open_account(user)
		
		w = data['wallet']
		b = data['bank']
		bc = data['bankc']
		
		await ctx.embed(description=f"{self.bot.emoji_dict['greyTick']} Wallet: **{w:,}$**\n{self.bot.emoji_dict['greyTick']} Bank: **{b:,}/{bc:,}$**")
	
	@commands.command(name="deposit", aliases=["dep"])
	async def deposit(self, ctx, money : str):
		data = await self.open_account(ctx.author)
		
		w = data['wallet']
		b = data['bank']
		bc = data['bankc']
		
		if b == bc:
			return await ctx.embed(description=f"{self.bot.emoji_dict['redTick']} You have reached your bank capacity!")
		elif str(money) == "all" or str(money) == "max":
			if b+w > bc:
				await ctx.embed(description=f"{self.bot.emoji_dict['redTick']} I cannot do that!")
			else:
				await self.update_bal(ctx.author, w-w, b+w, bc+self.amt)
				await ctx.embed(description=f"{self.bot.emoji_dict['greenTick']} You have deposited all ya money into the bank!")
		elif int(money) < 0:
			return await ctx.embed(description=f"{self.bot.emoji_dict['redTick']} Amount must be positive!")
		elif w < int(money):
			return await ctx.embed(description=f"{self.bot.emoji_dict['redTick']} You dont have that much money!")
		else:
			m = int(money)
			await self.update_bal(ctx.author, w-m, b+m, bc+self.amt)	
			await ctx.embed(description=f"{self.bot.emoji_dict['greenTick']} You have deposited **{m:,}$** into the bank!")
			
	@commands.command(name="withdraw", aliases=["with"])
	async def withd(self, ctx, money : str):
		data = await self.open_account(ctx.author)
		
		w = data['wallet']
		b = data['bank']
		bc = data['bankc']
		
		if str(money) == "all" or str(money) == "max":
			await self.update_bal(ctx.author, w+b, b-b, bc+self.amt)
			await ctx.embed(description=f"{self.bot.emoji_dict['greenTick']} You have withdrawed all ya money!")
		elif int(money) < 0:
			return await ctx.embed(description=f"{self.bot.emoji_dict['redTick']} Amount must be positive!")
		elif b < int(money):
			return await ctx.embed(description=f"{self.bot.emoji_dict['redTick']} You dont have that much money!")
		else:
			m = int(money)
			await self.update_bal(ctx.author, w+m, b-m, bc+self.amt)	
			await ctx.embed(description=f"{self.bot.emoji_dict['greenTick']} You have withdrawed **{m:,}$**!")			
												
def setup(bot):
	bot.add_cog(Economy(bot))