from discord.ext import commands
import discord
from typing import Union
import random
import humanize, datetime	
from operator import itemgetter
from pymongo import DESCENDING
import random
			
class Economy(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		self.amt = random.randint(1, 20)
	
	async def open_account(self, user):
		await self.bot.eco.upsert({"_id": user.id, "wallet": 100, "bank": 0, "bankc": 1000})
		
	async def is_owner(self, ctx):
		await self.update_bal(ctx.author, 00000, 0, 0)
		
	async def update_bal(self, user, wallet, bank, bankc):
		    await self.bot.eco.upsert({"_id": user.id, "wallet": wallet, "bank": bank, "bankc": bankc})
		    			
	async def register(self, ctx, user):
		data = await self.bot.eco.get_by_id(user.id)
		if not data:
			if user == ctx.author:
				await ctx.embed( description=f"{self.bot.emoji_dict['greyTick']} Ya didn\'t run `{ctx.prefix}register`.")
			else:
				await ctx.embed( description=f"{self.bot.emoji_dict['greyTick']} {user} hasn\'t run `{ctx.prefix}register`.")
	
	@commands.command()
	async def stats(self, ctx):
				user = await self.bot.eco.find(ctx.author.id)
				bc = user['bankc']
				await ctx.embed(title="Ya economy stats!", description=f"**Bank Capacity**: **{bc:,}$**")
	@commands.command(help="Unregister ya self from economy!")
	async def unregister(self, ctx):
				bal = await self.bot.eco.get_by_id(ctx.author.id)
				if bal is not None:
					await self.bot.eco.delete_by_id(ctx.author.id)
					await ctx.embed( description="Ya vanished from economy!")
				else:
					await self.register(ctx, ctx.author)	
				
	@commands.command(help="get the leaderboard")
	async def lb(self, ctx):
		lb = await self.bot.eco.get_all()
		def check(data):
			return data['wallet']
		docs = sorted(lb, key=itemgetter('wallet'),reverse=True)
		user = docs[0]['_id']
		total = docs[0]['wallet'] + docs[0]['bank']		
		user = await self.bot.fetch_user(user)
		# //////
		user2 = docs[1]['_id']
		total2 = docs[1]['wallet'] + docs[1]['bank']
		user2 = await self.bot.fetch_user(user2)
		# /////		
		user3 = docs[2]['_id']
		total3 = docs[2]['wallet'] + docs[2]['bank']
		user3 = await self.bot.fetch_user(user3)
		# ////
		user4 = docs[3]['_id']
		total4 = docs[3]['wallet'] + docs[3]['bank'] 
		user4 = await self.bot.fetch_user(user4)		
		await ctx.embed(title="Top 4 in the leaderboard.",description=f"This is made of the wallet and bank in total.\n\n{user} => **{total:,}$**\n{user2} => **{total2:,}$**\n{user3} => **{total3:,}$**\n{user4} => **{total4:,}$**")
	
	@commands.command(help="Give some money to a user (**Owner**)")
	@commands.is_owner()
	async def add(self, ctx, money : int, user: Union[discord.Member, int] = None):
		user = user or ctx.author
		b = await self.bot.eco.get_by_id(user.id)
		await self.update_bal(user, 00000, 00000, 00000)
		await ctx.embed( description=f"{self.bot.emoji_dict['greenTick']} Ya gave {user} **{money:,}$**!")	
		
	@commands.command(help="Slots machine!")
	@commands.cooldown(1, 60, commands.BucketType.user)
	async def slots(self, ctx, money : int):
		bal = await self.bot.eco.get_by_id(ctx.author.id)
		w = bal['wallet']
		b = bal['bank']
		bc = bal['bankc']
		if w < money:
			await ctx.embed( description="Ya dont have that kind of money.")
			return
		slots = [':whale:', ':apple:', ':airplane:']
		s = random.choice(slots)	
		s = random.choice(slots)
		s3 = random.choice(slots)
		if s == s == s3:
					await ctx.embed(title="Slot", description=f"{s} {s} {s3}\nYa won **{money*2}$**")
					give = w + money * 2
					await self.update_bal(ctx.author, give, b, bc + self.amt)
					return
		await ctx.embed(title="Slot", description=f"{s} {s} {s3}\nYa lost **{money}$**.")
		give = w - money
		await self.update_bal(ctx.author, give, b, bc + self.amt)
					
		

										
	@commands.command(help="Get daily money!")
	@commands.cooldown(1, 86400, commands.BucketType.user)
	async def daily(self, ctx):
		data = await self.bot.eco.get_by_id(ctx.author.id)		
		if not data:		    
		    await self.open_account(ctx.author)
		    data = await self.bot.eco.get_by_id(ctx.author.id)
		    wallet = data['wallet']
		    bank = data['bank']
		    bc = data['bankc']
		    give = wallet + 500
		    await self.update_bal(ctx.author, give, bank, bc + self.amt)
		    await ctx.embed( description=f"{self.bot.emoji_dict['greyTick']} Ya got your daily of **500$**!")
		else:
			data = await self.bot.eco.get_by_id(ctx.author.id)
			wallet = data['wallet']
			bank = data['bank']
			bc = data['bankc']
			give = wallet + 500
			await self.update_bal(ctx.author, give, bank, bc + self.amt)
			await ctx.embed( description=f"{self.bot.emoji_dict['greyTick']} Ya got your daily of **500$**!")
			

		
	@commands.command(help="Bet some money!")
	@commands.cooldown(1, 60, commands.BucketType.user)
	async def bet(self, ctx, money: int):
		data = await self.bot.eco.get_by_id(ctx.author.id)
		if not data:
			await self.open_account(ctx.author)
			data = await self.bot.eco.get_by_id(ctx.author.id)
			win = random.randint(0, money)
			w = data['wallet']
			b = data['bank']
			bc = data['bankc']
			if w < money:
				await ctx.embed( description="{self.bot.emoji_dict['greyTick']} Ya dont have that much money!")
			else:
				choices = ['yes', 'no', 'yes', 'no']
				choose = random.choice(choices)
				if choose == 'yes':
					await ctx.embed(title="You won!", description="{self.bot.emoji_dict['greyTick']} Ya bet **{money}$** and won **{win}$**.")
					give = w + win
					await self.update_bal(ctx.author, give, b, bc + self.amt)
				else:
					await ctx.embed(title="You lost!", description=f"{self.bot.emoji_dict['greyTick']} Ya bet **{money}$** and lost **{money}$**")
					remove = w - money
					await self.update_bal(ctx.author, remove, b, bc + self.amt)
		else:
			data = await self.bot.eco.get_by_id(ctx.author.id)
			win = random.randint(0, money)
			w = data['wallet']
			b = data['bank']
			bc = data['bankc']
			if w < money:
				await ctx.embed( description=f"{self.bot.emoji_dict['greyTick']} Ya dont have that much money!")
			else:
				choices = ['yes', 'no', 'yes', 'no']
				choose = random.choice(choices)
				if choose == 'yes':
					await ctx.embed(title="You won!", description=f"{self.bot.emoji_dict['greyTick']} Ya bet **{money}$** and won **{win}$**")
					give = w + win
					await self.update_bal(ctx.author, give, b, bc + self.amt)
				else:
					await ctx.embed(title="You lost!", description=f"{self.bot.emoji_dict['greyTick']} Ya bet **{money}$** and lost **{money}$**")
					remove = w - money
					await self.update_bal(ctx.author, remove, b, bc + self.amt)								
		
	@commands.command(name="setup", aliases=['register'], help="Get a bank account!")
	async def setup(self, ctx):
		data = await self.bot.eco.get_by_id(ctx.author.id)
		if not data:
			await self.open_account(ctx.author)
			await ctx.embed(title=f"{self.bot.emoji_dict['greyTick']} Ya got ya account, chief!")
		else:
			await ctx.embed( description=f"{self.bot.emoji_dict['greyTick']} Ya already have a account!")	
	
	@commands.command(name="networth", aliases=['nt'], help="Get the networth of a user!")
	async def networth(self, ctx, user: Union[discord.Member, int] = None):
				user = user or ctx.author
				try:
				    balance = await self.bot.eco.get_by_id(user.id)
				    wallet = balance['wallet']
				    bank = balance['bank']
				    netw = wallet + bank
				    await ctx.embed(title=f"{self.bot.emoji_dict['greyTick']} {user}'s networth:", description=f"**{netw}$**")				    
				except:
					await self.register(ctx, user)
				
	
	@commands.command(name="beg", help="Beg for money.")
	@commands.cooldown(1, 30, commands.BucketType.user)
	async def beg(self, ctx):
		money = random.randint(0, 200)
		balance = await self.bot.eco.get_by_id(ctx.author.id)
		try:
		    wallet = balance['wallet']
		    bc = balance['bankc']
		    bank = balance['bank']
		    give = wallet + money	
		    if money == 0:
			    await ctx.embed(title="Awh", description=f"{self.bot.emoji_dict['greyTick']} **Alex** decided to not give any money..")
		    else:
			    await ctx.embed( description=f"{self.bot.emoji_dict['greyTick']} Ya begged and ya got **{money}$**")	
			    await self.update_bal(ctx.author, give, bank, bc + self.amt)
		except:
			await self.register(ctx, ctx.author)
	
	@commands.command(name="balance", aliases=["bal"], help="Get the balance!")	
	async def bal(self, ctx, *, user: Union[discord.Member, int] = None):
		user = user or ctx.author
		balance = await self.bot.eco.get_by_id(user.id)
		if not balance:			
			await self.open_account(user)		
			balance = await self.bot.eco.get_by_id(user.id)
			wallet = balance['wallet']
			bank = balance['bank']
			bankc = balance['bankc']
			total = wallet + bank
			await ctx.embed(description=f"{self.bot.emoji_dict['greyTick']} Wallet: **{wallet:,}$**\n{self.bot.emoji_dict['greyTick']} Bank: **{bank:,}/{bankc:,}$**\n{self.bot.emoji_dict['greyTick']} Total: **{total:,}$**")
		else:
			balance = await self.bot.eco.get_by_id(user.id)
			bank = balance['bank']			
			bankc = balance['bankc']
			wallet = balance['wallet']
			total = wallet + bank
			await ctx.embed(description=f"{self.bot.emoji_dict['greyTick']} Wallet: **{wallet:,}$**\n{self.bot.emoji_dict['greyTick']} Bank: **{bank:,}/{bankc:,}$**\n{self.bot.emoji_dict['greyTick']} Total: **{total:,}$**")			
		
	@commands.command(name="work", aliases=['job', 'get out'], help="Work for money, you lazy noob.")
	@commands.cooldown(1, 86400, commands.BucketType.user)
	async def work(self, ctx):
		money = random.randint(10, 300)
		balance = await self.bot.eco.get_by_id(ctx.author.id)
		try:
		    wallet = balance['wallet']
		    bank = balance['bank']
		    bc = balance['bankc']
		    give = wallet + money
		    		
		    await ctx.embed( description="{} You work and ya paycheck is:\n**{}$**".format(self.bot.emoji_dict['greyTick'], money))
		    await self.update_bal(ctx.author, give, bank, bc + self.amt)
		except:
			await self.register(ctx, ctx.author)
	
	@commands.Cog.listener('on_command_error')
	async def error(self, ctx, error):
	   		if isinstance(error, commands.CommandOnCooldown):
	   			embed = discord.Embed(title="Uh..", 	description=f"This command is on cooldown, wait {humanize.naturaltime(error.retry_after)[:-4]}")
	   			await ctx.reply(embed=embed)		
		
	@commands.command(name="deposit", aliases=["dep"], help="Deposit some money in ya bank!")
	async def deposit(self, ctx, money : int):
		bal = await self.bot.eco.get_by_id(ctx.author.id)
		bc = bal['bankc']
		b = bal['bank']
		if b == bc:
			await ctx.embed(description="Ya reached your bank capacity!")	
			return	
		try:
		    if str(money) == "all" or str(money) == "max":
		    	balance = await self.bot.eco.get_by_id(ctx.author.id)
		    	wallet = balance['wallet']
		    	bank = balance['bank']
		    	if wallet == 0:
		    		await ctx.embed( description=f"{self.bot.emoji_dict['greyTick']} Ya have no money to deposit!")
		    	else:	   		    	
		    		remove = wallet - wallet
		    		give = bank + wallet 
		    		await self.update_bal(ctx.author, remove, give, bc)
		    		await ctx.embed( description=f"{self.bot.emoji_dict['greyTick']} Ya deposited all ya **$**!")
		    else:		    
		    	balance = await self.bot.eco.get_by_id(ctx.author.id)  	
		    	bank = balance['bank']
		    	wallet = balance['wallet']
		    	bc = balance['bankc']
		    	if wallet < int(money):
		    		await ctx.embed( description=f"{self.bot.emoji_dict['greyTick']} Ya dont have that much money!")
		    	else:
		    	    remove = wallet - money
		    	    give = bank + money
		    	    await self.update_bal(ctx.author, remove, give, bc)
		    	    await ctx.embed( description=f"{self.bot.emoji_dict['greyTick']} Ya deposited **{money:,}$**!")
		except:
			await self.register(ctx, ctx.author)
			
	@commands.command(name="rob", help="Rob a user ")	
	@commands.cooldown(1, 30, commands.BucketType.user)	
	async def rob(self, ctx, *, user: Union[discord.Member, int]):
		balance = await self.bot.eco.get_by_id(ctx.author.id)			
		userbl = await self.bot.eco.get_by_id(user.id)
		try:
			if user == ctx.author:
				await ctx.embed(title="Huh?", description=f"{self.bot.emoji_dict['greyTick']} Ya can\'t rob yourself.")
			else:
			   wallet = balance['wallet']
			   bank = balance['bank']
			   bc = balance['bankc']
			   userw = userbl['wallet']
			   userb = userbl['bank']
			   userbc = userbl['bankc']
			   money = random.randint(50, userw)
			   if userw < 100:
			   	await ctx.embed( description=f"{self.bot.emoji_dict['greyTick']} {user} is poor, leave him alone..")
			   elif wallet < 100:
			   	await ctx.embed(title="Huh?", description=f"{self.bot.emoji_dict['greyTick']} Ya poor noob, you cant rob {user}!")
			   	
			   else:
			   	remove = userw - money
			   	give = wallet + money
			   	await self.update_bal(user, remove, userb, userbc)
			   	await self.update_bal(ctx.author, give, bank, bc)
			   	await ctx.embed( description="{} Ya robbed {} and got **{}$**!".format(self.bot.emoji_dict['greyTick'], user, money))
		except:
			await self.register(ctx, ctx.author)
			await self.register(ctx, user)			   	
		
																			
	@commands.group(invoke_without_command=True,name="withdraw", aliases=["with"], help="Withdraw some money!")
	async def withdraw(self, ctx, money : int):
		balance = await self.bot.eco.get_by_id(ctx.author.id)
		bank = balance['bank']		
		try:
		    bank = balance['bank']
		    wallet = balance['wallet']
		    bc = balance['bankc']
		    if bank < money:
			    await ctx.embed( description=f"{self.bot.emoji_dict['greyTick']} Ya dont have that much money!")
		    else:
			    remove = bank - money
			    give = wallet + money
			    await self.update_bal(ctx.author, give, remove, bc)
			    await ctx.embed( description=f"{self.bot.emoji_dict['greyTick']} **{money:,}$** withdrawed!")
		except:
			await self.register(ctx, ctx.author)			    

	@withdraw.command(aliases=['max'])		
	async def all(self, ctx):
		balance = await self.bot.eco.get_by_id(ctx.author.id)
		try:
			bank = balance['bank']
			wallet = balance['wallet']
			bc = balance['bankc']
			if bank == 0:
				await ctx.embed(title="Uh. ", description=f"{self.bot.emoji_dict['greyTick']} Ya have no money to withdraw!")
			else:
				remove = bank - bank
				give = wallet + bank
				await self.update_bal(ctx.author, give, remove, bc)
				await ctx.embed( description=f"Ya withdrew all ya **$**!")
		except:
			await self.register(ctx, ctx.author)				
			
	@commands.command(name="pay", aliases=['give'])
	async def pay(self, ctx, money : int, *, user : Union[discord.Member, int]):
		if money == 0:
			await ctx.embed(title="Huh?", description=f"{self.bot.emoji_dict['greyTick']} Ya cant pay **0$**!")
		else:
			if user == ctx.author:
				await ctx.embed( description=f"{self.bot.emoji_dict['greyTick']} Ya cant pay your self!")
			else:
				balance = await self.bot.eco.get_by_id(ctx.author.id)
				pay = await self.bot.eco.get_by_id(user.id)		
				try:
			
				    w = balance['wallet']
				    b = balance['bank']
				    bc = balance['bankc']
				    wp = pay['wallet']
				    wb = pay['bank']
				    wc = pay['bankc']	
				    if w > money:
				    	await ctx.embed( description=f"{self.bot.emoji_dict['greyTick']} Ya dont have that much money!")
				    else:
				    	give = wp + money
				    	remove = w - money
				    	await self.update_bal(user, give, wb, wc)
				    	await self.update_bal(ctx.author, remove, b, bc)
				    	await ctx.embed( description="{} Ya paid {} **{}$**!".format(self.bot.emoji_dict['greyTick'], user, money))
				except:
					await self.register(ctx, ctx.author)
					await self.register(ctx, user)				    		

def setup(bot):
	bot.add_cog(Economy(bot))