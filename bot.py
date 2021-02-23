from discord.ext import commands, ipc
import discord
import utils.json_loader
from utils.PacBot import PacMe
from utils.help import Help
import os
	
bot = PacMe()	
secret_file = utils.json_loader.read_json("secrets")
bot.paginated_help = Help()
bot.config_token = secret_file['token']


def load_extensions():
	for extension in bot.startup_extensions:
		try:
			bot.load_extension(extension)
		except Exception as e:
			print(e)

# running the bot.

if __name__ == '__main__':
	load_extensions()
	bot.run(bot.config_token)