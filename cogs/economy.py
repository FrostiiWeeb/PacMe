from discord.ext import commands
import discord
from typing import Union, Optional
import random

import datetime
from discord.ext import commands
from utils.PacBot import PacMe

on_cooldown = {}  # A dictionary mapping user IDs to cooldown ends

class cooldowns:
    
    def datetime_to_int(self, dt):
    	return int(dt.strftime("%Y%m%d%H%M%S"))
    
    def cooldown(self, seconds):
        async def predicate(context):
            if (cooldown_end := await context.bot.db.fetchrow("SELECT cooldown FROM cool_down WHERE user_id = $1", context.author.id))  or int(cooldown_end) < datetime.datetime.now():
                if context.valid and context.invoked_with in (*context.command.aliases, context.command.name):
                	now = datetime.datetime.now()
                	now = self.datetime_to_int(self, now)
                	delta = datetime.timedelta(seconds=seconds)
                	delta = delta.seconds
                	                	             	
                	await context.bot.db.execute("UPDATE cool_down SET cooldown = $1 WHERE user_id = $2 AND command = $3",now + delta, context.author.id, str(context.command))
                return True
            else:
            	raise commands.CommandOnCooldown(commands.BucketType.user, (cooldown_end - self.datetime_to_int(datetime.datetime.now())))

        return commands.check(predicate)

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
	@cooldowns.cooldown(cooldowns, 20)
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
