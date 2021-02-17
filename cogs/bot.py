import platform
import discord
from discord.ext import commands, flags
from collections import OrderedDict, deque, Counter
import psutil
from psutil import Process
import asyncio
import time
import os
import humanize
import datetime
import pathlib
import inspect

import pathlib
p = pathlib.Path('./')
cm = cr = fn = cl = ls = fc = 0
for f in p.rglob('*.py'):
    if str(f).startswith("venv"):
        continue
    fc += 1
    with f.open() as of:
        for l in of.readlines():
            l = l.strip()
            if l.startswith('class'):
                cl += 1
            if l.startswith('def'):
                fn += 1
            if l.startswith('async def'):
                cr += 1
            if '#' in l:
                cm += 1
            ls += 1


class Misc(commands.Cog):
	
	def __init__(self, bot):
		self.bot = bot
		self.process = Process(os.getpid())
		
	@commands.command(aliases=['src'], help="Get the source!", brief="Get the source!")
	async def source(self, ctx, *, command: str = None):
		source_url = 'https://github.com/FrostiiWeeb/PacMe'
		branch = 'master'
		if command is None:
			return await ctx.embed(title=f"**Respect the license {self.bot.emoji_dict['rooEZ']}**",description=f"[Now click here.](https://github.com/FrostiiWeeb/PacMe/)")
									
		elif command.startswith('jsk') or command.startswith('jishaku'):
			e=discord.Embed(description='[This is not my code so here you go](https://pypi.org/project/jishaku/)')
			await ctx.send(embed=e)
		else:
			obj = self.bot.get_command(command.replace('.', ' '))
			if obj is None:
				return await ctx.send('Could not find command.')
			src = obj.callback.__code__
			module = obj.callback.__module__
			filename = src.co_filename
		
			lines, firstlineno = inspect.getsourcelines(src)
			if not module.startswith('discord'):
				location = os.path.relpath(filename).replace('\\', '/')
			else:
				location = module.replace('.', '/')
				source_url = 'https://github.com/FrostiiWeeb/PacMe'
				branch = 'master'

			final_url = f'<{source_url}/blob/{branch}/{location}#L{firstlineno}-L{firstlineno + len(lines) - 1}>'
			e=discord.Embed(title="**Respect the license {}**".format(self.bot.emoji_dict['rooEZ']),description=f"{final_url}")
			await ctx.send(embed=e)
	

	@commands.command(name='activity', aliases=['a'], help="Change the bot activity!", brief="change the bot presence")
	@commands.is_owner()
	async def presence(self, ctx, atype: str, *, activity=None):
		atype = atype.lower()
		if atype == 'server':
			length = len(self.bot.guilds)
			await self.bot.change_presence(activity=discord.Game(name=f"{length} servers! | !*help"))		
		if atype == 'default':
			await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=f'@{self.bot.user.name}'))
		if atype == 'watching':
			await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f"{activity}"))
		if atype == 'listening':
			await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=activity))
		if atype == 'playing':
			await self.bot.change_presence(activity=discord.Game(name=activity))
		if atype == 'streaming':
			await self.bot.change_presence(activity=discord.Streaming(name=activity, url='!*help'))
		if atype == 'competing':
			await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.competing, name=activity))
		await ctx.embed(description=f'Set activity to `{activity}` with type `{atype}` ')

	
	@commands.command(help="Get the credit!", brief="Get the credits.")	
	async def credit(self, ctx):
		await ctx.embed(title="Credit", description="averwhy#3899 - Maintenace command.\nRainbow#8292 - Info command.\nVaskel#5683 - License, ctx.embed()\nppotatoo - Presence command")
	
	@commands.Cog.listener()
	async def on_ready(self):
						print(f"{self.__class__.__name__} Cog has been loaded\n-----")		

						
																		
	@commands.command(brief="Latency for the bot!",help="Get the latency of the bot.")
	async def ping(self, ctx):
		start = time.perf_counter()
		await self.bot.eco.get_by_id(self.bot.user.id)
		end = time.perf_counter()
		db = round(end - start, 2) * 1000
		time_1 = time.perf_counter()
		await ctx.trigger_typing()
		time_2 = time.perf_counter()
		ping = round((time_2-time_1)*1000)	
		msgg = await ctx.send("Ping!")
		embed = discord.Embed(color=0x2f3136, title="Pong!", description=f"{self.bot.emoji_dict['loading']} **| Websocket:**\n```py\n{round(self.bot.latency * 1000, 2)}ms\n```\n{self.bot.emoji_dict['typing']} **| Typing:**```py\n{ping}ms\n```<:mongo:809056657422024705> | **Database:**\n```\n{db}ms\n```")
		await msgg.edit(embed=embed)		
	
	@commands.command(brief="Get some info bout' the bot.",help="Info about the bot.", aliases=['about'])
	async def info(self, ctx):
	       x = await self.bot.fetch_user(784122061219954708)
	       process = psutil.Process(os.getpid())
	       embed = discord.Embed(color = 0x2f3136, title=f'Info', description=f'{ctx.bot.description}\nNote: My prefix is **"{ctx.prefix}"**')
	       embed.add_field(name='Info:', value=f"{self.bot.emoji_dict['greyTick']} **Developer\'s -** [FrostiiWeeb](https://discord.com/users/746807014658801704), [Cyrus](https://discord.com/users/668906205799907348)\n{self.bot.emoji_dict['greyTick']} **Last boot -** {humanize.naturaltime(datetime.datetime.utcnow() - self.bot.launch_time)}\n{self.bot.emoji_dict['greyTick']} **Library -** [discord.py](https://pypi.org/project/discord.py/)\n{self.bot.emoji_dict['greyTick']} **Created - ** {humanize.naturaltime(x.created_at)}\n{self.bot.emoji_dict['greyTick']} **Command Credit -** **Rainbow#8292 - Info command**,\n**averwhy#3899 - Maintenace**,\n**Vaskel#5683 - License, ctx.embed**", inline=False)
	       embed.add_field(name='Stats:', value=f"{self.bot.emoji_dict['greyTick']} **Number of commands -** {len(self.bot.commands)}\n{self.bot.emoji_dict['greyTick']} **Guilds -** {len(list(map(str, [p.id for p in self.bot.guilds])))}\n{self.bot.emoji_dict['greyTick']} **Users -** {len(list(map(str, [p.id for p in self.bot.users])))}\n{self.bot.emoji_dict['greyTick']} **Using {humanize.naturalsize(process.memory_info().rss)} physical memory, {humanize.naturalsize(process.memory_info().vms)} virtual memory.**",inline=False)
	       embed.add_field(name="Code Stats:", value=f"{self.bot.emoji_dict['greyTick']} **Files:** {fc}\n{self.bot.emoji_dict['greyTick']} **Lines:** {ls:,}\n{self.bot.emoji_dict['greyTick']} **Classes:** {cl}\n{self.bot.emoji_dict['greyTick']} **Functions:** {fn}\n{self.bot.emoji_dict['greyTick']} **Coroutines:** {cr}\n{self.bot.emoji_dict['greyTick']} **Comments:** {cm:,}", inline=False)
	       embed.add_field(name='Links:', value=f"{self.bot.emoji_dict['greyTick']} **Invite Link -** [Here](https://top.gg/bot/784122061219954708)\n{self.bot.emoji_dict['greyTick']} **Source (Github) -** [Here](https://github.com/FrostiiWeeb/PacMe)",inline=False)
	       await ctx.send(embed=embed)
	
	@commands.command(brief="Invite URL for the bot.",help="The invite of the bot.",aliases=['inv'])
	async def invite(self, ctx):
		emned = discord.Embed(title="```Invite URL:```", description="[Click Here](https://top.gg/bot/784122061219954708)", colour=0x2f3136)
		await ctx.send(embed=emned)
	
	@commands.command(brief="Changelog, nothing special.",help="The bot changelog.", aliases=['cl'])
	async def changelog(self, ctx):
	           embed = discord.Embed(
	           title=f"**Changelog {self.bot.emoji_dict['rooEZ']}:**",
	           description="```Re-added custom prefixes (**with database**)```",
	           colour=0x2f3136
	           )
	           await ctx.send(embed=embed)
	           
		
def setup(bot):
	bot.add_cog(Misc(bot))
