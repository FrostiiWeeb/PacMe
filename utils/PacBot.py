# Standard 
import os
import logging

# Basic

import discord
from discord.ext.commands import Bot as BotBase
from discord.ext import commands
from pathlib import Path
import mystbin
import motor.motor_asyncio

# Local code

import utils.json_loader
from utils.CustomContext import PacContext
from utils.mongo import Document

cwd = Path(__file__).parents[0]
cwd = str(cwd)
print(f"{cwd}\n-----")



async def get_prefix(bot, message):
    # If dm's
    if not message.guild:
        return commands.when_mentioned_or("!*")(bot, message)

    try:
        data = await bot.config.find(message.guild.id)

        # Make sure we have a useable prefix
        if not data or "prefix" not in data:
            bot.cache[message.guild.id] = bot.empty_cache            
            return commands.when_mentioned_or("!*")(bot, message)
        bot.cache[message.guild.id] = await bot.config.get_by_id(message.guild.id)
        return commands.when_mentioned_or(data["prefix"])(bot, message)
    except:
        bot.cache[message.guild.id] = bot.empty_cache
        return commands.when_mentioned_or("!*")(bot, message)

secret_file = utils.json_loader.read_json("secrets")
class PacMe(BotBase):
	def __init__(self, **kwargs):
		super().__init__(
		**kwargs,
		command_prefix = get_prefix,
		owner_ids={668906205799907348, 746807014658801704},
		case_insensitive=True
		)
		
		# Cogs
		
		self.coglist = [f"cogs.{item[:-3]}" for item in os.listdir("/storage/emulated/0/PacMe/cogs") if item != "__pycache__"] + ["jishaku"] + ["listeners.error"]
		for extension in self.coglist:
		      		try:
		      			self.load_extension(extension)
		      		except Exception as e:
		      			print(e)
		
		# Cache
		
		self.empty_cache = {"prefix": "!*"}
		self.cache = {}
		
		# Config
		
		self.connection_url = secret_file["mongo"]
		self.config_token = secret_file["token"]
		self.maint = False
		self.maintenence = False
		self.mystbin = mystbin.Client()
		
		# Database
		
		self.mongo = motor.motor_asyncio.AsyncIOMotorClient(str(self.connection_url))
		self.db = self.mongo["frostiiweeb"]
		self.config = Document(self.db, "config")
		
	async def on_ready(self):
		print(f"----\nBot is online\n\nUser: {self.user}\nID: {self.user.id}\nWorking on: {len(self.guilds)} guilds.\n----")
	
	async def get_context(self, message, *, cls=None):
		return await super().get_context(message, cls=cls or PacContext)	