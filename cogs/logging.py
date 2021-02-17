from discord.ext import commands
import discord

class Logging(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
	
	@commands.command(help="Set the logging channel!", name="log")
	@commands.has_permissions(administrator=True)
	async def setup_log(self, ctx, channel : int):
		await ctx.embed(description=f"**Note: The \"channel\" argument is an channel id.\nSet logging channel id to: **{channel}**")
		await self.bot.log.upsert({"_id": ctx.guild.id, "channel_id": channel})
		
	@commands.Cog.listener('on_member_remove')
	async def remmove(self, member):
		log = await self.bot.log.get_by_id(member.guild.id)
		if not log:
			return
		def predicate(event):
			return event.action is discord.AuditLogAction.ban or event.action is discord.AuditLogAction.kick
		event = await member.guild.audit_logs().find(predicate)
		chan = log['channel_id']		
		embed = discord.Embed(description=f"**Case - {member.guild.name}**\nUser: **{member} (ID: {member.id})**\nReason: **{event.reason}**\nModerator: **{event.user}**")
		sent = await self.bot.fetch_channel(chan)
		await sent.send(embed=embed)		
		
def setup(bot):
	bot.add_cog(Logging(bot))			