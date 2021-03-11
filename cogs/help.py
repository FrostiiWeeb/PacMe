from discord.ext import commands
import discord
from utils.help import PaginatedHelp

class Help(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		self._original_help = bot.help_command
		self.bot.help_command = PaginatedHelp()
		
	def cog_unload(self):
		self.bot.help_command = self._original_help		

def setup(bot):
	bot.add_cog(Help(bot))