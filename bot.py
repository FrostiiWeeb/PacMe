from discord.ext import commands
import json
from utils.PacBot import PacMe

bot = PacMe()

with open("bot_config/secrets.json", "r") as f:
	token = json.load(f)
bot.token = token['token']

bot.run(bot.token)