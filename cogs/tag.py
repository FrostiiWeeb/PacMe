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

class TagName(commands.clean_content):
    def __init__(self, *, lower=False):
        self.lower = lower
        super().__init__()

    async def convert(self, ctx, argument):
        converted = await super().convert(ctx, argument)
        lower = converted.lower().strip()

        if not lower:
            raise commands.BadArgument('Missing tag name.')

        if len(lower) > 100:
            raise commands.BadArgument('Tag name is a maximum of 100 characters.')

        first_word, _, _ = lower.partition(' ')

        # get tag command.
        root = ctx.bot.get_command('tag')
        if first_word in root.all_commands:
            raise commands.BadArgument('This tag name starts with a reserved word.')

        return converted if not self.lower else lower


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
	async def tag(self, ctx, *, name : TagName(lower=True)):
		try:
			# Select the content from the database.
			data = await self.bot.db.fetchrow("SELECT content FROM tags WHERE name = $1", str(tag))
			# Send the content.
			await ctx.send(data["content"])			
		except Exception as e:
			tags = [db['name'] for db in await self.bot.db.fetch("SELECT * FROM tags")]
			matches = get_close_matches(name, tags)
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
	async def claim(self, ctx, tag : TagName(lower=True)):
		try:
			# Select the content from the database.
			data = await self.bot.db.fetchrow("SELECT author FROM tags WHERE name = $1", str(tag))
			if not data['author'] == str(ctx.author):
				await ctx.send("The tag owner is still here!")
			else:
				await ctx.send("Transfered tag to ya!")
				await self.bot.db.execute("UPDATE tags SET author = $1 WHERE user_id = $1", str(ctx.author), data['user_id'])	
		except Exception as e:
			print(e)
			tags = [db['name'] for db in await self.bot.db.fetch("SELECT * FROM tags")]
			matches = get_close_matches(name, tags)
			if len(matches) > 0:
				await ctx.send(f"A tag with that name does not exist, did you mean \"{matches[0]}\"?")
			else:
				await ctx.send("A tag with that name does not exist.")		
	
	@tag.command()
	async def edit(self, ctx, tag : TagName(lower=True), *, content : commands.clean_content):
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
	async def transfer(self, ctx, target : discord.Member, *, tag : TagName(lower=True)):
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
	async def info(self, ctx, *, tag : TagName(lower=True)):
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
			converter = TagName()
			original = ctx.message
			await ctx.send("What should the tag name be?")
			name = await self.bot.wait_for("message", check=lambda m : m.author == ctx.author, timeout=15.0)
		except asyncio.TimeoutError:
			await ctx.embed(description=f"You took so much time! Use `{ctx.prefix}tag make` to try again.")
		else:
			
			ctx.message = name
			name = await converter.convert(ctx, name.content)
			
		try:
			await ctx.send("What should the tag content be?")
			msg = await self.bot.wait_for("message", check=lambda m : m.author == ctx.author, timeout=15.0)
		except asyncio.TimeoutError:
			await ctx.embed(description=f"You took so much time! Use `{ctx.prefix}tag make` to try again.")
		else:
			if msg.content:
				clean_content = await commands.clean_content().convert(ctx, msg.content)
			else:
				clean_content = msg.content
		try:
			row = await self.bot.db.fetchrow("SELECT 1 FROM tags WHERE name = $1", name)
			if row is not None:
				return await ctx.send(f"The tag `{name}` already exists.")
			else:
				await self.bot.db.execute("INSERT INTO tags(user_id, name, content, author) VALUES ($1, $2, $3, $4) ", ctx.author.id, name, clean_content, str(ctx.author))
				await ctx.embed(description=f"Created tag `{name}`!")
		except:
			return
						
															
def setup(bot):
	bot.add_cog(Tags(bot))