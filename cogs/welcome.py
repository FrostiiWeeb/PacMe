import discord
from discord.ext import commands
import asyncio

class Welcome(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		
	@commands.Cog.listener('on_member_join')
	async def member_join(self, member):
		data = await self.bot.w.get_by_id(member.guild.id)
		if data:
			channel = await self.bot.fetch_channel(data['channel_id'])
			msg = data['welcome_message']
			await chanel.send(f"{msg}")
		else:
			return
	
	@commands.group(invoke_without_command=True, name="welcome")
	async def welcome(self, ctx):
		"""
		A welcome thing lmao idk
		"""
	
	@welcome.command(name="setup")
	@commands.is_owner()
	async def set_channel(self, ctx):
		author = ctx.author
		try:
			def check(m):
				return m.author == ctx.author and m.channel == ctx.channel
			await ctx.embed(description="Send the channel ID where the welcome message is sent.")
			id = await self.bot.wait_for("message", timeout=10.0, check=check)			
			channel_id = id.content
			await ctx.embed(description="Send the message to be the welcome msg.\nUse \"default\" to use the default msg.")			
			msg = await self.bot.wait_for("message", timeout=10.0, check=check)
			if msg.content == "default":
				await ctx.embed(description="The message has been set to: " f"Hey! {ctx.author.name}! You have joined {ctx.guild.name}, welcome!")
				msg = "Hey! {member.name}! You have joined {member.guild.name}, welcome!"
			else:
				msg = msg
			await self.bot.w.upsert({"_id": ctx.guild.id, "channel_id": channel_id, "welcome_message": msg})
			await ctx.confirm(f"Is this correct?\nchannel_id: {channel_id}\nwelcome_msg: {msg}")
		except asyncio.TimeoutError:
				return
				
				
def setup(bot):
	bot.add_cog(Welcome(bot))