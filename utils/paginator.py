import discord
from discord.ext import commands
from typing import Union, List, Optional
from contextlib import suppress
import asyncio

class Paginator:
	"""
	An object for pagination for discord.py.
	
	_pages: List[discord.Embed] : `The pages of the paginator.`
	index : int : `The index page of the paginator.`
	current : int : The current page of the paginator.
	timeout : float = 90.0 : `The timeout for the paginator.`
	ctx : NoneType : `The context for the paginator.`
	message : NoneType : `The message for the paginator.`
	compact : bool : `If the paginator's pages are less then 3 then compact will take over.
	_buttons : dict : The reactions for the paginator.`
	
	"""	
	__slots__ = ('_pages', 'previous', 'current', 'timeout', 'ctx', 'message', 'compact', '_buttons','has_input', '_tasks', 'end')
	
	
	def __init__(self, *, entries: Optional[Union[List[discord.Embed], discord.Embed]] = None, timeout: float = 90.0,has_input : bool = True):
			
		self._pages = entries
		self.current = 0
		self.previous = 0
		self.timeout = timeout
		self.ctx = None
		self.end = 0
		self.has_input = has_input
		self.compact : bool = False
		self.message = None
		self._tasks = []
		if len(self._pages) == 2:
			self.compact = True
		
		self._buttons = {
		"⏪": 0.0,
		"◀️": -1,		
		"▶️": +1,
		"⏩": None,
		"⏹️": "stop"
		}

		if self.has_input is True:
				self._buttons["🔢"] = "input"				
		if self.compact is True:
			keys = ('⏩', '⏪', '🔢')
			for key in keys:
				del self._buttons[key]
				
				
	async def controller(self, react):
				if react == "stop":
					await self.message.delete()
					
				elif react == "input":
					await self.go_to_input()
				
				elif isinstance(react, int):
				        self.current += react
				        if self.current < 0 or self.current > self.end:
				        	self.current -= react
				        else:
				        	self.current = int(react)
	
	def check(self, payload):
	           if payload.message_id != self.message.id:
	           	return False
	           if payload.user_id != self.ctx.author.id:
	           	return False
	           
	           return str(payload.emoji) in self._buttons																				
				
	async def go_to_input(self):
		"""
		An function for the input.
		"""
		to_delete = []
		message = await self.ctx.send("What page do you want to go to?")
		to_delete.append(message)
		
		def check(m):
		                
		                  if m.author.id != self.ctx.author.id:
		                  	return False
		                  if self.ctx.channel.id != m.channel.id:
		                  	return False
		                  if not m.content.isdigit():
		                  	return False
		                  return True
		 
		try:
		          message = await self.ctx.bot.wait_for("message", check=check, timeout=30.0)
		except asyncio.TimeoutError:
		          await self.ctx.send("You took too long to enter a number.")
		else:
		              to_delete.append(message)
		              self.current = int(message.content)
		              await self.message.edit(embed=self._pages[self.current])



	
	async def start(self, ctx):
		    """
		    Start the paginator.
		    """
		    self.ctx = ctx
		    
		    await self._paginate()			    		    		    
	async def _paginate(self):
		    """
		    Start the pagination session.
		    """
		    with suppress(discord.HTTPException, discord.Forbidden, IndexError):
		    	self.message = await self.ctx.send(embed=self._pages[0])
		    	if len(self._pages) > 1:
		    		for b in self._buttons:
		    			await self.message.add_reaction(b)
		    while True:
		    	tasks = [
		    	asyncio.ensure_future(
		    	self.ctx.bot.wait_for("raw_reaction_add", check=self.check)),
		    	asyncio.ensure_future(
		    	self.ctx.bot.wait_for("raw_reaction_remove", check=self.check)),]
		    	
		    	done, pending = await asyncio.wait(
		    	tasks, timeout=self.timeout, return_when=asyncio.FIRST_COMPLETED)
		    	
		    	for task in pending:
		    		task.cancel()
		    	
		    	if len(done) == 0:
		    		return await self.message.delete()
		    	
		    	payload = done.pop().result()
		    	
		    	reaction = self._buttons.get(str(payload.emoji))
		    	
		    	self.previous = self.current
		    	await self.controller(reaction)
		    	if self.previous == self.current:
		    		continue
		    	await self.message.edit(embed=self._pages[self.current])

             		    						    				
		    		
