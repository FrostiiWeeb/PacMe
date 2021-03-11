import discord
from discord.ext import commands
import asyncio
from typing import List, Union, Optional
from contextlib import suppress

class Paginator:
	def __init__(self, pages: Optional[Union[List[discord.Embed], discord.Embed]] = None,timeout: float = 90.0):
		self.pages = pages
		self.current = 0
		self.previous = 0
		self.end = 0
		self.timeout = timeout		
		
		self.ctx = None
		self.bot = None
		self.msg = None
		
		self.reactions = {
            "⏮️": 0.0,
            "◀️": -1,
            "⏹️": "stop",
            "▶️": +1,
            "⏭️": None,
        }		
	
	async def stop(self):
		self.pages = []
	
	async def wait_for_reaction(self, ctx, wait_for):
		def check(reaction, user):
			return user == self.ctx.author
			
		try:
		
			reaction, user = await self.ctx.bot.wait_for("reaction_add", timeout=self.timeout, check=check)
			if str(reaction.emoji) == "⏹️":
				await self.msg.delete()
			if str(reaction.emoji) == "▶️":
				try:					
					await self.msg.edit(embed=self.pages[self.current-1])
					self.current = len(self.pages)-len(self.pages)-1
					await wait_for(ctx)
				except Exception as r:
					raise RuntimeError(r)	
			if str(reaction.emoji) == "◀️":
				try:
					await self.msg.edit(embed=self.pages[self.current+1])		
				except Exception as r:
					raise RuntimeError(r)
		except asyncio.TimeoutError:
								pass		
	
	async def start(self, ctx):
		self.ctx = ctx
		
		if len(self.pages) == 0:
			raise RuntimeError("Can\'t paginate an empty list.")
		self.msg = await ctx.send(embed=self.pages[self.current])
		
		
		
		self.reacts = [
		"⏮️",
		"◀️",
		"⏹️",
		"▶️"
		"⏭"
		]
		
		for r in self.reactions:
			await self.msg.add_reaction(r)		
		
		def check(reaction, user):
			return user == self.ctx.author
			
		try:
		
			reaction, user = await self.ctx.bot.wait_for("reaction_add", timeout=self.timeout, check=check)
			if str(reaction.emoji) == "⏹️":
				await self.msg.delete()
			if str(reaction.emoji) == "▶️":
				try:					
					await self.msg.edit(embed=self.pages[self.current-1])
					self.current = len(self.pages)-len(self.pages)-1
					await self.wait_for_reaction(ctx, self.wait_for_reaction)
				except Exception as r:
					raise RuntimeError(r)	
			if str(reaction.emoji) == "◀️":
				try:
					await self.msg.edit(embed=self.pages[self.current+1])		
				except Exception as r:
					raise RuntimeError(r)
		except asyncio.TimeoutError:
								pass
								