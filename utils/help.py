from typing import Optional

from discord import Embed
from discord.utils import get
from discord.ext.menus import MenuPages, ListPageSource
from discord.ext.commands import Cog
from discord.ext import commands
from discord.ext.commands import command


def syntax(command):
	cmd_and_aliases = "|".join([str(command), *command.aliases])
	params = []

	for key, value in command.params.items():
		if key not in ("self", "ctx"):
			params.append(command.usage or f"<{key}>")

	params = " ".join(params)

	return f"{cmd_and_aliases} {params}"

class HelpMenu(ListPageSource):
	def __init__(self, ctx, data):
		self.lmao = ctx

		super().__init__(data, per_page=3)

	async def write_page(self, menu, fields=[]):
		offset = (menu.current_page*self.per_page) + 1
		len_data = len(self.entries)

		embed = Embed(title="Help",
					  description=f"Welcome to the {self.lmao.bot.user.name} help menu!\n\n```\nNews\n```\n**Economy commands!**\n")
		embed.set_thumbnail(url=self.lmao.guild.me.avatar_url)
		embed.set_footer(text=f"{offset:,} - {min(len_data, offset+self.per_page-1):,} of {len_data:,} commands.")

		for name, value in fields:
			embed.add_field(name=name, value=value, inline=False)

		return embed

	async def format_page(self, menu, entries):
		fields = []

		for entry in entries:
			fields.append((entry.brief or entry.help or "No description.", syntax(entry)))

		return await self.write_page(menu, fields)

async def cmd_help(ctx, command):
					  embed = Embed(title=f"Help",
					  description=syntax(command) + "\n" + command.help or command.brief)
					  await ctx.send(embed=embed)
					 
async def cog_help(ctx, cog):
	embed = Embed(title=cog.qualified_name)
	await ctx.send(embed=embed)	
	
class PaginatedHelp(commands.HelpCommand):
	async def send_bot_help(self, mapping):
		menu = MenuPages(source=HelpMenu(ctx=self.context, data=list(self.context.bot.commands)),
		delete_message_after=True,
		timeout=60.0)
		
		await menu.start(self.context)
	
	async def send_command_help(self, command):
		return await cmd_help(ctx=self.context, command=command)