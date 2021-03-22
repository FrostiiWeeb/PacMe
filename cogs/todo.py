import discord
from discord.ext import commands
import asyncio
from typing import Optional
from typing import Union
from asyncpg import UniqueViolationError
import discord
from discord import Embed
from discord.utils import get
from discord.ext.menus import MenuPages, ListPageSource
from discord.ext import menus

class TodoSource(ListPageSource):
		def __init__(self, ctx, data):
			self.lmao = ctx
			
			super().__init__(data, per_page=3)
		
		async def write_page(self, menu, fields=[]):
			embed = Embed(title="Todos")
			for name in fields:
				embed.add_field(name=name, value="______")
			return embed
		
		async def format_page(self, menu, entries):
			fields = []
			for entry in entries:
				fields.append(entry)
			
			return await self.write_page(menu, fields)
			
class TodoPages(MenuPages):
    def __init__(self, source):
        super().__init__(source, delete_message_after=True, timeout=60.0)			

class Todos(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
	
	async def get_user_todos(self, ctx, user):
		todo_list = []
		for db in await self.bot.db.fetch("SELECT * FROM todos WHERE user_id = $1", ctx.author.id):
			todo_list.append(f"[{db['amount']}] {db['content']}")		
		await TodoPages(source=TodoSource(ctx=ctx, data=todo_list)).start(ctx)
		
	@commands.command()
	async def todos(self, ctx):
		"""
		Get the todos of the author (`ctx.author`)
		"""
		await self.get_user_todos(ctx, ctx.author)
	
	@commands.group(invoke_without_command=True)
	async def todo(self, ctx):
		pass
	
	@todo.command(name="add")
	async def todo_add(self, ctx, *, content):
		try:
			row = await self.bot.db.fetchrow("SELECT 1 FROM todos WHERE user_id = $1", ctx.author.id)
			if not row:
				await self.bot.db.execute("INSERT INTO todos(user_id, amount, content) VALUES ($1, $2, $3)", ctx.author.id, 1, content)
			else:
				r = row['amount']
				new_amt += 1
				await self.bot.db.execute("INSERT INTO todos(user_id, amount, content) VALUES ($1, $2, $3)", ctx.author.id, new_amt-1, content)	
			await ctx.embed(description="Added todo!")
			
		except Exception as e:
			await ctx.embed(description=e)
	
def setup(bot):
	bot.add_cog(Todos(bot))							