from discord.ext import commands



class Help(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		self._original_help = bot.help_command
		bot.help_command = bot.paginated_help
		bot.help_command.cog = self
	
	def cog_unload(self):
		self.bot.help_command = self._original_help

def setup(bot):
	bot.add_cog(Help(bot))