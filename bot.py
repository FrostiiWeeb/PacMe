import utils.jishaku_reactions
from discord.ext import commands
import json

# Local code

from utils.PacBot import PacMe
import utils.json_loader

import asyncio
import io
import contextlib
from traceback import format_exception
import textwrap
import discord
from discord.ext.buttons import Paginator
import re

# Making the bot an variable.	
			
bot = PacMe()

class Pag(Paginator):
	def __init__(self, **kwargs):
		super().__init__(**kwargs)

# Add all the emoji's from the database.

async def fill_emojis():
	
	records = await bot.db.fetch("SELECT id, name FROM emojis")
	for r in records:
		bot._emojis = {f"{r['name']}": f"<:{r['name']}:{r['id']}>"}

# Fill the blacklist.

async def fill_blacklist():

        records = await bot.db.fetch("SELECT user_id FROM blacklist")
        bot.blacklist = {r["user_id"] for r in records}

# Connect to the db.

async def run(bot):
	db = await __import__('asyncpg').create_pool(user=bot.asyncpg['user'], password=bot.asyncpg['password'], database='PacMe', host='127.0.0.1')
	bot.db = db
	await bot.db.execute("CREATE TABLE IF NOT EXISTS blacklist(user_id bigint PRIMARY KEY)")
	await bot.db.execute("CREATE TABLE IF NOT EXISTS tags(user_id bigint, name TEXT, content TEXT, author TEXT)")
	await bot.db.execute("CREATE TABLE IF NOT EXISTS economy(user_id bigint PRIMARY KEY, wallet bigint, bank bigint)")
	await bot.db.execute("CREATE TABLE IF NOT EXISTS emojis(name TEXT PRIMARY KEY, id bigint)")
	await bot.db.execute("CREATE TABLE IF NOT EXISTS prefixes(guild_id bigint PRIMARY KEY, prefix TEXT)")
	await fill_blacklist()
	await fill_emojis()

# Loop the db.

loop = asyncio.get_event_loop()
loop.run_until_complete(run(bot=bot))

@bot.ipc.route()
async def get_guild_count(data):
	return len(bot.guilds)

# On_message : `An event for messages.`

@bot.event
async def on_message(message):
		if re.fullmatch("<@(!)?784122061219954708>", message.content):
		
			await message.channel.send(f"My prefix is `{await bot.get_prefix(message)}`.")
			
		if message.author.id in bot.blacklist or getattr(message.guild, "id", None) in bot.blacklist:
		  return
		await bot.process_commands(message)
		


# Run the bot.

if __name__ == "__main__":
	bot.run(bot._token)