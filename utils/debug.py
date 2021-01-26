import json
import os
from datetime import datetime
from itertools import cycle
import discord
import logging
from discord.ext import commands, tasks
from pathlib import Path
from discord.ext.commands import Bot
import inspect
import asyncio
import os
import psutil
import humanize
import psutil
import sys

class Debug(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
	@commands.Cog.listener()
	async def on_ready(self):
						print(f"{self.__class__.__name__} Cog has been loaded\n-----")	
			
	@commands.command(name="debug", aliases=['dbg'], brief="Custom debug cog.", help="Custom debug cog.", ignore_extra=False)
	@commands.is_owner()
	async def debug(self, ctx:commands.Context):
		process = psutil.Process(os.getpid())
		await ctx.embed(title="debug", description=f"```\nDebug version: 1.20.0\nDiscord.py version: {discord.__version__}\nPython {sys.version} on {sys.platform}\n\nUsing {humanize.naturalsize(process.memory_info().rss)} physical memory and {humanize.naturalsize(process.memory_info().vms)} virtual memory.\n\n{self.bot.user.name} can see {len(self.bot.guilds):,} guild(s) and {len(self.bot.users):,} user(s).\n```")

def setup(bot):
	bot.add_cog(Debug(bot))	