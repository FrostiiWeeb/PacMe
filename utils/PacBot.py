# Standard 
import os
import logging

# Basic

import discord
from discord.ext.commands import Bot 
from discord.ext import commands
from pathlib import Path
import mystbin
import motor.motor_asyncio
import utils.errors
try:
	import psutil
	import aiosqlite
except:
	pass
import os
import asyncpg

# Local code

import utils.json_loader
from utils.CustomContext import PacContext
from utils.mongo import Document

cwd = Path(__file__).parents[0]
cwd = str(cwd)
print(f"{cwd}\n-----")


		
os.environ["JISHAKU_NO_UNDERSCORE"] = "True"
# also 
os.environ["JISHAKU_NO_DM_TRACEBACK"] = "True" 
os.environ["JISHAKU_HIDE"] = "True"

async def get_prefix(bot, message):
	try:
		prefix = await bot.db.fetch("SELECT prefix FROM prefixes WHERE guild_id = $1", message.guild.id)
		return commands.when_mentioned_or(f"{prefix['prefix']}")(bot, message)			
	except Exception as e:
		return '!*'

class BotBase(Bot):
	def __init__(self, *args, **kwargs):
		super().__init__(allowed_mentions=discord.AllowedMentions(users=True, everyone=False, replied_user=False, roles=False), intents=discord.Intents.all(), *args, **kwargs)

secret_file = utils.json_loader.read_json("secrets")
class PacMe(BotBase):
	def __init__(self, **kwargs):
		super().__init__(
		**kwargs,
		command_prefix = get_prefix,
		owner_ids=[668906205799907348, 746807014658801704],
		case_insensitive=True,
		)
		
		# Cogs
		
		self.coglist = [f"cogs.{item[:-3]}" for item in os.listdir("/storage/emulated/0/PacMe/cogs") if item != "__pycache__"] + ["jishaku"] + ["listeners.error"]
		for extension in self.coglist:
		      		try:
		      			self.load_extension(extension)
		      		except Exception as e:
		      			print(e)
		
		# Cache

		self.cache = {}
		
		# Config
		self._token = secret_file["token"]
		self.dagpi = secret_file["dagpi"]
		self.asyncpg = secret_file['postgres']
		self.blacklist = set()
		self.embed_color = 0x8936FF
		self.embed_colour = self.embed_color
		self.maint = False
		self.maintenence = False
		self._underscore = True
		self.mystbin = mystbin.Client()
		self.emoji_dict = {"greyTick": "<:greyTick:596576672900186113>", "greenTick": "<:greenTick:596576670815879169>", "redTick": "<:redTick:596576672149667840>", "dpy": "<:dpy:596577034537402378>", "py": "<:python:286529073445076992>"}
		self.custom_errors = utils.errors
				
		
	async def on_ready(self):
		    
		    print(
        "Logged in! \n"
        f"{'-' * 20}\n"
        f"Bot Name: {self.user} \n"
        f"Bot ID: {self.user.id} \n"
        f"{'-' * 20}"
    )
	
	async def get_context(self, message, *, cls=None):
		return await super().get_context(message, cls=cls or PacContext)
