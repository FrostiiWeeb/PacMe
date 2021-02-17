from typing import Optional

import discord
from discord import Embed
from discord.utils import get
from discord.ext.menus import MenuPages, ListPageSource
from discord.ext.commands import Cog
from discord.ext import commands

def syntax(command):
	cmd_and_aliases = "|".join([str(command), *command.aliases])
	params = []

	for key, value in command.params.items():
		if key not in ("self", "ctx"):
			params.append(f"[{key}]" if "Nonetype" in str(value) else f"<{key}>")

	params = " ".join(params)

	return f"`{cmd_and_aliases} {params}`"

class HelpMenu(ListPageSource):
	def __init__(self, ctx, data):
		self.ctx = ctx

		super().__init__(data, per_page=4)

	async def write_page(self, menu, fields=[]):
		offset = (menu.current_page*self.per_page) + 1
		len_data = len(self.entries)

		embed = Embed(title="Help",
					  description=f"Welcome to the {self.ctx.bot.user.name} help menu!\nUse ```{self.ctx.prefix}help [cmd]``` for command help.\n**About**\n{self.ctx.bot.description}\n",
					  colour=0x2f3136)
		embed.set_thumbnail(url=self.ctx.bot.user.avatar_url)
		embed.set_footer(text=f"{offset:,} - {min(len_data, offset+self.per_page-1):,} of {len_data:,} commands.")

		for name, value in fields:
			embed.add_field(name=name, value=value, inline=False)

		return embed
		
	async def format_page(self, menu, entries):
		fields = []

		for entry in entries:
			if entry.hidden:
				pass
			fields.append((entry.brief or entry.help or "No description.", syntax(entry)))

		return await self.write_page(menu, fields)		

async def cog_help(ctx, cog):
	commands = ", ".join([c.qualified_name for c in cog.get_commands()])
	embed = Embed(title=f"Help with {cog.qualified_name}", description=f"**Commands**\n{commands}\n\n**Description**\n{cog.description}" if cog.description else f"**Commands**\n{commands}")
	return await ctx.send(embed=embed)

async def cmd_help(ctx, command):
	if command.hidden:
		return
	else:
					  ai = ", ".join(command.aliases)
					  embed = Embed(title=f"Help with {command}",
					  description=f"{syntax(command)}\n**Aliases**\n{ai}" if command.aliases else syntax(command),
					  colour=0x2f3136)
					  embed.add_field(name="Command description", value=command.help, inline=False)
					  await ctx.send(embed=embed)

class Help(commands.HelpCommand):
	async def send_bot_help(self, mapping):
		menu = MenuPages(source=HelpMenu(self.context, list(self.context.bot.commands)),
		delete_message_after=True,
		timeout=60.0)
		await menu.start(self.context)
	
	async def send_command_help(self, command : commands.Command):
		await cmd_help(ctx=self.context, command=command)
	
	async def send_cog_help(self, cog):
		await cog_help(ctx=self.context, cog=cog)