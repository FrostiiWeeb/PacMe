# We import our modules.

import json
import os
import datetime
from datetime import datetime
from itertools import cycle
import discord
import logging
from discord.ext import commands, tasks, ipc
from pathlib import Path
from discord.ext.commands import Bot
import inspect
import asyncio
import os
import psutil
import humanize
from utils.CustomContext import PacContext
import motor.motor_asyncio
from utils.mongo import Document
import mystbin
import utils.json_loader as utils
import aiozaneapi
from typing import Optional
import cogs.library_override

import discord
from discord import Embed
from discord.utils import get
from discord.ext.menus import MenuPages, ListPageSource
from discord.ext.commands import Cog
from discord.ext import commands


# Shows the current working directory.

cwd = Path(__file__).parents[0]
cwd = str(cwd)
print(f"{cwd}\n-----")

# Define our default prefix.

default_prefix = "!*"

# Gets the prefix for the bot.

async def get_prefix(bot, message):
    if message.author.id in bot.owner_ids and not message.content.startswith('!*'):
    	return ''
    # If dm's
    if not message.guild:
        return commands.when_mentioned_or("!*")(bot, message)

    else:
        try:
            data = await bot.config.find(message.guild.id)

            # Make sure we have a useable prefix
            if not data or "prefix" not in data:
                return commands.when_mentioned_or("!*")(bot, message)
            return commands.when_mentioned_or(data["prefix"])(bot, message)
        except Exception as e:
            print(e)		


# Makes a class for the colours.
	

class Colors:
    default = 0x2f3136
    teal = 0x1abc9c
    dark_teal = 0x11806a
    green = 0x2ecc71
    dark_green = 0x1f8b4c
    blue = 0x3498db
    dark_blue = 0x206694
    purple = 0x9b59b6
    dark_purple = 0x71368a
    magenta = 0xe91e63
    dark_magenta = 0xad1457
    gold = 0xf1c40f
    dark_gold = 0xc27c0e
    orange = 0xe67e22
    dark_orange = 0xa84300
    red = 0xe74c3c
    dark_red = 0x992d22
    lighter_grey = 0x95a5a6
    dark_grey = 0x607d8b
    light_grey = 0x979c9f
    darker_grey = 0x546e7a
    blurple = 0x7289da	

secret_file = utils.read_json("secrets")
class PacMe(Bot):
	def __init__(self):
		super().__init__(
		command_prefix=get_prefix,
		intents=discord.Intents.all(),
		description = "A multi-purpose bot with Fun commands, Moderation, and more!",
		case_insensitive=True,
		fetch_offline_members=True,
		allowed_mentions=discord.AllowedMentions(roles=False,
		users=True,
		everyone=False,
		replied_user=False)
		)				
		self.example_embed = discord.Embed(title="```Title```", description=f"```Description```", colour=discord.Colour.from_rgb(64, 64, 64))
		self.launch_time = datetime.utcnow()
		self.owner_ids = {746807014658801704, 668906205799907348}
		self.version = "1.2.3"
		self.colour = discord.Colour.red()
		self.maintenence = False
		self.maint = False
		self.colors = Colors
		self.colours = self.colors
		self.log_channel = self.get_channel(789892435190349859)
		self.loop.create_task(self.handle_display())
		self.load_extension('utils.debug')
		self.connection_url = secret_file["mongo"]
		self.zane = aiozaneapi.Client(secret_file["zane"])
		self.ipc = ipc.Server(self, secret_key="Frost")
		self.emoji_dict = {
            "redTick": "<:redTick:596576672149667840>",
            "greenTick": "<:greenTick:596576670815879169>",    
            "greyTick": '<:greyTick:596576672900186113>',   
            'loading': '<a:loading:747680523459231834>',
            'typing': '<a:typing:597589448607399949>',
            'arrow': '<:member_join:596576726163914752>',
            'rooEZ': '<:rooEZ:596577109695266837>',
            'downvote': '<:downvote:596577438952062977>',
            'upvote': '<:upvote:596577438461591562>',
            'bot': '<:bot_tag:596576775555776522>',
            'cool': '<a:rooCool:747680120763973654>'
        }
		self.grey = 0x2f3136
		self.utils = utils	
		self.mystbin = mystbin.Client()
		self.cwd = cwd+"/bot.py"	
		self.start_time = datetime.utcnow()	
		self.display_messages = (
    ("Bot is now online!", ""),
    ("My prefix is:", default_prefix),
    ("Discord.py version:", discord.__version__),
    ("Bot version:", "1.2.3")
)
		self.mongo = motor.motor_asyncio.AsyncIOMotorClient(str(self.connection_url))
		self.db = self.mongo["frostiiweeb"]		
		self.config = Document(self.db, "config")
		self.eco = Document(self.db, "economy")
		self.td = Document(self.db, "todo")
		self.log = Document(self.db, "logging")
		print("Initialized Database\n-----")
	
	@tasks.loop(seconds=80)
	async def change_str(self):
		ccl = itertools.cycle(["@PacMe", "{length} servers and {users}!"])
		length = len(self.guilds)	
		users = len(self.users)	
		await self.change_presence(activity=discord.Game(name=ccl, length=length, users=users))
	
	async def on_ipc_error(self, endpoint, error):
		print(endpoint, "raised", error)		
	
	async def handle_display(self):
		width, _ = os.get_terminal_size()
		border = "=" * width
		output = border.center(width)
		kwargs = {
		"bot": "PacMe#9790",
		"discord": discord
		}
		for group in self.display_messages:

		          for i, message in enumerate(group):
		          	message = message.format(**kwargs)
		          	centered = message.center(width)
		          	end = "\n" if i == 0 else "\n\n"
		          	output += centered + end
		output += border.center(width)
		print(output)
																
	async def on_message(self, message):
	       ctx = await self.get_context(message, cls=PacContext)
	       
	       await self.invoke(ctx)