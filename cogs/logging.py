from discord.ext import commands
import discord

class Logging(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
	
	@commands.Cog.listener()
	async def on_member_ban(self, guild, user : discord.User):
		def predicate(event):
			return event.action is discord.AuditLogAction.ban
		
		try:
			event = await guild.audit_logs().find(predicate)
			data = await self.bot.db.fetchrow("SELECT * FROM logging WHERE guild_id = $1", guild.id)
			ctx = await self.bot.fetch_channel(data['channel_id'])
			await ctx.send(f"{event}")
		except Exception as e:
			print(e)
			return

def setup(bot):
	bot.add_cog(Logging(bot))		