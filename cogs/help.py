from discord.ext import commands
from utils.help import PaginatedHelp

class Help(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		self._original_help = bot.help_command
		self.bot.help_command = PaginatedHelp()
	


def setup(bot):
	bot.add_cog(Help(bot))