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
from difflib import get_close_matches

class TagSource(ListPageSource):
		def __init__(self, ctx, data):
			self.lmao = ctx
			
			super().__init__(data, per_page=4)
		
		async def write_page(self, menu, fields=[]):
			embed = Embed(title="Tags")
			for name in fields:
				embed.add_field(name=name, value="______")
			return embed
		
		async def format_page(self, menu, entries):
			fields = []
			for entry in entries:
				fields.append(entry)
			
			return await self.write_page(menu, fields)
			
class TagPages(MenuPages):
    def __init__(self, source):
        super().__init__(source, delete_message_after=True, timeout=60.0)			

class Tags(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
	
	async def get_user_tags(self, ctx, user):
		tag_list = []
		for db in await self.bot.db.fetch("SELECT * FROM tags WHERE author = $1", str(user)):
			tag_list.append(db["name"])		
		await TagPages(source=TagSource(ctx=ctx, data=tag_list)).start(ctx)
	
	async def get_global_tags(self, ctx):
		tag_list = []
		for db in await self.bot.db.fetch("SELECT * FROM tags;"):
			tag_list.append(db["name"])
		await TagPages(source=TagSource(ctx=ctx, data=tag_list)).start(ctx)
	
	@commands.group(invoke_without_command=True, help="Get the content for a tag.")
	async def tag(self, ctx, *, tag):
		try:
			# Select the content from the database.
			data = await self.bot.db.fetchrow("SELECT content FROM tags WHERE name = $1", str(tag))
			# Send the content.
			await ctx.send(data["content"])			
		except Exception as e:
			tags = [db['name'] for db in await self.bot.db.fetch("SELECT * FROM tags")]
			matches = get_close_matches(tag, tags)
			if len(matches) > 0:
				await ctx.send(f"A tag with that name does not exist, did you mean \"{matches[0]}\"?")
			else:
				await ctx.send("A tag with that name does not exist.")
	
	@commands.command()
	async def tags(self, ctx):
		"""
		Get the tags of the author (`ctx.author`)
		"""
		await self.get_user_tags(ctx, ctx.author)
	
	@tag.command()
	async def edit(self, ctx, tag : str, *, content):
			"""
			Edit a tag.
			"""
			try:
				data = await self.bot.db.fetchrow("UPDATE tags SET content = $1 WHERE name = $2 AND author = $3", content, str(tag), str(ctx.author))
				await ctx.send(f"Edited `{tag}`!")			
			except Exception as e:
				print(e)
				await ctx.send("A tag with that name does not exist or you don\'t own it.")		
	
	@tag.command()
	async def transfer(self, ctx, target : discord.Member, *, tag):
			"""
			Transfer a tag to another member.
			"""
			try:
				data = await self.bot.db.fetchrow("UPDATE tags SET author = $1 WHERE name = $2 AND user_id = $3", str(target), str(tag), ctx.author.id)
				await ctx.send(f"Transfered `{tag}`!")			
			except Exception as e:
				print(e)
				await ctx.send("A tag with that name does not exist or you don\'t own it.")
						
	@tag.command()
	async def info(self, ctx, *, tag):
		"""
		Get the info of an tag.
		"""
		try:
			data = await self.bot.db.fetchrow("SELECT * FROM tags WHERE name = $1", str(tag))
			owner = data['author']
			name = data['name']		
			await ctx.embed(description=f"**Name:**\n{name}\n**Owner:**\n{owner}\n")				
		except Exception as e:
			print(e)
			await ctx.send("A tag with that name does not exist.")		
	
	@tag.command()
	async def list(self, ctx):
		await self.get_global_tags(ctx)
	
	@tag.command()
	async def make(self, ctx):
		try:
			await ctx.send("What should the tag name be?")
			msg = await self.bot.wait_for("message", check=lambda m : m.author == ctx.author, timeout=15.0)
		except asyncio.TimeoutError:
			await ctx.embed(description=f"You took so much time! Use `{ctx.prefix}tag make` to try again.")
		else:
			for cmd in self.bot.commands:
				if msg.content == cmd.qualified_name:
					return await ctx.send("`{}` is an prohibited name.".format(msg.content))
					break					
			if msg.content.startswith("tag"):
				return await ctx.send("`{}` is an prohibited name.".format(msg.content))
							
			name = msg.content.strip("\"")
			
		try:
			await ctx.send("What should the tag content be?")
			msgg = await self.bot.wait_for("message", check=lambda m : m.author == ctx.author, timeout=15.0)
		except asyncio.TimeoutError:
			await ctx.embed(description=f"You took so much time! Use `{ctx.prefix}tag make` to try again.")
		else:
			content = msgg.content
		try:
			row = await self.bot.db.fetchrow("SELECT 1 FROM tags WHERE name = $1", name)
			if row is not None:
				return await ctx.send(f"The tag `{name}` already exists.")
			else:
				await self.bot.db.execute("INSERT INTO tags(user_id, name, content, author) VALUES ($1, $2, $3, $4) ", ctx.author.id, name, content, str(ctx.author))
				await ctx.embed(description=f"Created tag `{name}`!")
		except:
			return
						
															
def setup(bot):
	bot.add_cog(Tags(bot))