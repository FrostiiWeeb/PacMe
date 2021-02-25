# Standard 
import os
import logging

import discord
from discord.ext.commands import Bot as BotBase
from pathlib import Path
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
        return commands.when_mentioned_or(bot.DEFAULTPREFIX)(bot, message)

    try:
        data = await bot.config.find(message.guild.id)

        # Make sure we have a useable prefix
        if not data or "prefix" not in data:
            bot.cache[message.guild.id] = bot.empty_cache            
            return commands.when_mentioned_or("!*")(bot, message)
        bot.cache[message.guild.id] = await self.bot.config.get_by_id(message.guild.id)
        return commands.when_mentioned_or(data["prefix"])(bot, message)
    except:
        bot.cache[message.guild.id] = bot.empty_cache
        return commands.when_mentioned_or("!*")(bot, message)

secret_file = utils.json_loader.read_json("secrets")
class PacMe(BotBase):
	def __init__(self, **kwargs):
		super().__init__(
		command_prefix = "!*",
		owner_ids={668906205799907348, 746807014658801704},
		)
		self.empty_cache = {"prefix:" "!*"}
		self.cache = {}
		self.connection_url = secret_file["mongo"]
		self.config_tokem = secret_file["token"]
		self.mongo = motor.motor_asyncio.AsyncIOMotorClient(str(self.connection_url))
		self.db = self.mongo["frostiiweeb"]
		self.config = Document(self.db, "config")			