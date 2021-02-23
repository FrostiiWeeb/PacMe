import discord
from discord.ext import commands

class Todo(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
	
	async def add_td(self, user, todo):
		await self.bot.td.upsert({"_id": user.id, "text": todo})
	
	async def open_id(self, user):
		await self.bot.td.upsert({"_id": user.id, "text": "**Todo List**"})
	
	@commands.group(invoke_without_command=True, name="todo")
	async def todo(self, ctx):
		pass
	
	@todo.command()
	async def add(self, ctx, num, *, todo):
		td = await self.bot.td.get_by_id(ctx.author.id)
		await ctx.embed(description=f"Added {todo} as the {num} todo.")
		if td:
			t = td['text']
			await self.add_td(ctx.author, f"{t}\n**{num}**. {todo}")
		else:
			await self.open_id(ctx.author)
			td = await self.bot.td.get_by_id(ctx.author.id)
			await self.add_td(ctx.author, f"**{num}**. {todo}")
	
	@todo.command()
	async def list(self, ctx):
		td = await self.bot.td.get_by_id(ctx.author.id)
		text = td['text']
		await ctx.embed(description=text)	
			
			
			
def setup(bot):
	bot.add_cog(Todo(bot))		