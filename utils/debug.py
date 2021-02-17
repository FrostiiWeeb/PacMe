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
from psutil import Process
import sys
from jishaku.codeblocks import codeblock_converter
from jishaku.modules import package_version
from jishaku.paginators import PaginatorInterface, WrappedPaginator
from subprocess import call
from jishaku.codeblocks import Codeblock, codeblock_converter
from jishaku.exception_handling import ReplResponseReactor
from jishaku.features.baseclass import Feature
from jishaku.paginators import PaginatorInterface, WrappedPaginator
from jishaku.shell import ShellReader
from jishaku.exception_handling import ReplResponseReactor
from jishaku.features.baseclass import Feature
from jishaku.models import copy_context_with
from jishaku.paginators import PaginatorInterface, WrappedPaginator


class Debug(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		self.process = Process(os.getpid())
	
	@commands.Cog.listener()
	async def on_message(self, message):
	       if message.author.bot:
	       	return
	       
	       if message.content.startswith(f"<@{self.bot.user.id}>") and len(message.content) == len(
        f"<@{self.bot.user.id}>"):
        	data = await self.bot.config.get_by_id(message.guild.id)
        	if not data or "prefix" not in data:
        		prefix = "!*"
        	else:
        		prefix = data["prefix"]
        	embed = discord.Embed(title="Whoops!", description=f"Ya mentioned me, well, my prefix here is `{prefix}`\nBut you can also mention me!")
        	await message.channel.send(embed=embed, delete_after=30)


	@commands.Cog.listener()
	async def on_ready(self):
						print(f"{self.__class__.__name__} Cog has been loaded\n-----")	
			
	@commands.group(name="debug", aliases=['dbg'], brief="Custom debug cog.", help="Custom debug cog.", ignore_extra=False, invoke_without_command=True)
	@commands.is_owner()
	async def debug(self, ctx:commands.Context):
	       self.bot.say = ctx.send
	       if isinstance(self.bot, discord.AutoShardedClient):
	       	msg = "PacMe is automatically sharded, and "
	       else:
	       	msg = "PacMe is not sharded, and "
	       summary = [
	       f"```\nDebug v{package_version('jishaku')}\ndiscord.py {package_version('discord.py')}``` "
	       f"```\nPython {sys.version} on {sys.platform}\n```",
	       f"```\nUsing {humanize.naturalsize(self.process.memory_info().rss)} physical memory, {humanize.naturalsize(self.process.memory_info().vms)} virtual memory and {humanize.naturalsize(Process().memory_full_info().uss)} of wich unique to this process\nRunning on PID {Process().pid} (python3) with {Process().num_threads()} threads.\n```\n"
	       f"```\n{msg}can see {len(self.bot.guilds):,} guild(s) and {len(self.bot.users):,} user(s).\nAverage websocket latency: {round(self.bot.latency * 1000, 2)}ms\n```"
	       ]
	       await ctx.embed(title="debug", description="\n".join(summary))
	
	@debug.command()
	async def rtt(self, ctx):
		await ctx.invoke(self.bot.get_command('jsk rtt'))
		
	@debug.command()
	async def py(self, ctx, *, argument : codeblock_converter):
		await ctx.invoke(self.bot.get_command('jsk py'), argument=argument)
		
	@debug.command()
	async def sh(self, ctx, argument : codeblock_converter):
		await ctx.invoke(self.bot.get_command('jsk sh'), argument=argument)	              
	
	@debug.command()
	async def cat(self, ctx, *, argument: str):
		await ctx.invoke(self.bot.get_command('jsk cat'), argument=argument)
		
	@debug.command()
	async def su(self, ctx, target: discord.User, *, command_string : str):
		await ctx.invoke(self.bot.get_command('jsk su'), target=target, command_string=command_string)
		
	@debug.command()
	async def dbg(self, ctx, *, command_string : str):
		await ctx.invoke(self.bot.get_command('jsk dbg'), command_string=command_string)

def setup(bot):
	bot.add_cog(Debug(bot))	
