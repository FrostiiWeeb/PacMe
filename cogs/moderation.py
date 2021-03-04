from discord import Embed
from utils.TimeConverter import TimeConverter
import discord
from discord.ext import commands
import asyncio
import random
from typing import Union

class Moderation(discord.ext.commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		self.muted_perms = discord.Permissions(send_messages=False, speak=False)
	
	async def _get_mute_role(self, guild: discord.Guild):
	       # automate retrieval and possible instantiation of muted role
	       mute_role = discord.utils.get(guild.roles, name="Muted")
	       
	       if not mute_role:
	               mute_role = await guild.create_role(
	               name="Muted",
	               permissions=self.muted_perms)
	       return mute_role
	
	async def do_action(self, ctx, action, author, user, reason):
		user = await self.bot.fetch_user(user)
		return await ctx.embed(
		description=f"**New {action}**\nUser: **{user}**\nReason: **{reason}**"
		)
	
	@commands.command(aliases=['tm'])
	@commands.has_permissions(manage_guild=True)
	async def tempmute(self, ctx, duration="5s", target : Union[discord.Member, int] = None, reason="Not found "):
		time = TimeConverter().convert(duration)
		if target == ctx.author:
			return await ctx.send("You can\'t do that to yourself!")
					
		role = await self._get_mute_role(ctx.guild)
		await target.add_roles(role)	
		await self.do_action(ctx, "Tempmute", ctx.author, target.id, reason)	
		await asyncio.sleep(time)
		await target.remove_roles(role)
		
		
		
							
		
	@commands.command(aliases=['b'])
	@commands.has_permissions(ban_members=True)
	@commands.bot_has_permissions(ban_members=True)
	async def ban(self, ctx, target : Union[discord.Member, int] = None, *, reason="Not Provided."):
		"""
		Bans a user
		"""
		target = target or ctx.author
		if target.id == ctx.author.id:
			return await ctx.send("You can\'t do that to yourself!")
		if target.top_role >= ctx.me.top_role:
			return await ctx.send("The user\'s role is higher or equal to mine.")
		with __import__('contextlib').suppress(discord.HTTPException):
			await target.send(f"You were banned from {ctx.guild.name} for {reason}")
		
		audit = f"{ctx.author} [{ctx.author.id}] - {reason}"
		await ctx.guild.ban(target, reason=audit)
		await self.do_action(ctx, "Ban", ctx.author, target.id, reason)
	
	@commands.command()
	@commands.guild_only()
	@commands.has_permissions(ban_members=True)
	@commands.bot_has_permissions(ban_members=True)
	async def unban(self, ctx, user: int, *, reason=None):
	       """Unbans a user with a given ID"""
	       if user == ctx.author.id:
	       	return await ctx.send("You can't do that to yourself!")
	       member = discord.Object(id=user)
	       try:
	         
	           await ctx.guild.unban(member, reason=f"{ctx.author} [{ctx.author.id}] - {reason}")
	           await self.do_action(ctx, "Unban", ctx.author, target.id, reason)
	       except discord.NotFound:
	       	return await ctx.send(embed=discord.Embed(description="That user doesn't seem to be banned."))

	
	@commands.command(aliases=['gstart'])
	@commands.is_owner()
	async def giveaway(self, ctx):
		await ctx.send("Let's start with this giveaway! Answer these questions within 15 seconds!")
		questions = ["Which channel should it be hosted in?",
		"What should be the duration of the giveaway? (s|m|h|d)",
		"What is the prize of the giveaway?"]
		
		answers = []
		
		def check(m):
			return m.author == ctx.author and m.channel == ctx.channel 
		
		for i in questions:
			await ctx.send(i)
			
			try:
				msg = await self.bot.wait_for('message', timeout=15.0, check=check)
			except asyncio.TimeoutError:
			         await ctx.send('You didn\'t answer in time, please be quicker next time!')
			         return
			else:
			  answers.append(msg.content)
		try:
		   c_id = int(answers[0][2:-1])
		except:
		      await ctx.send(f"You didn't mention a channel properly.")
		      return
		
		channel = self.bot.get_channel(c_id)
		
		time = TimeConverter().convert(str(answers[1]))
		if time == -1:
		      await ctx.send(f"You didn't answer the time with a proper unit. Use (s|m|h|d) next time!")
		      return
		elif time == -2:
		      await ctx.send(f"The time must be an integer. Please enter an integer next time")
		      return
		
		prize = answers[2]
		
		await ctx.send(f"The Giveaway will be in {channel.mention} and will last {answers[1]}!")
		
		embed = discord.Embed(title = "Giveaway!", description = f"{prize}", color = ctx.author.color)
		
		embed.add_field(name = "Hosted by:", value = ctx.author.mention)
		embed.set_footer(text = f"Ends {answers[1]} from now!")
		my_msg = await channel.send(embed = embed)
		await my_msg.add_reaction("🎉")
		
		await asyncio.sleep(time)
		new_msg = await channel.fetch_message(my_msg.id)
		users = await new_msg.reactions[0].users().flatten()
		users.pop(users.index(self.bot.user))
		winner = random.choice(users)
		await channel.send(embed=discord.Embed(description=f"Congratulations! {winner.mention} won {prize}!"))

def setup(bot):
	bot.add_cog(Moderation(bot))