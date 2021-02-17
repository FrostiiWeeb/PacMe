from discord.ext import commands, ipc
import discord
import utils.json_loader
from utils.PacBot import PacMe
from utils.help import Help
import os

def run():
	bot = PacMe()
	secret_file = utils.json_loader.read_json("secrets")
	bot.paginated_help = Help()
	for file in os.listdir("/storage/emulated/0/discord/cogs"):
		if file.endswith(".py") and not file.startswith('_'):
			bot.load_extension(f"cogs.{file[:-3]}")
	bot.config_token = secret_file['token']
	bot.run(bot.config_token)

# running the bot.

if __name__ == '__main__':
	run()