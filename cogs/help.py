from typing import Optional

import discord
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
			params.append(f"[{key}]" if "NoneType" in str(value) else f"<{key}>")

	params = " ".join(params)

	return f"`{cmd_and_aliases} {params}`"


class HelpMenu(ListPageSource):
	def __init__(self, ctx, data):
		self.ctx = ctx

		super().__init__(data, per_page=3)

	async def write_page(self, menu, fields=[]):
		offset = (menu.current_page*self.per_page) + 1
		len_data = len(self.entries)

		embed = Embed(title="Help",
					  description=f"Welcome to the {self.ctx.bot.user.name} help menu!",
					  colour=self.ctx.bot.grey)
		embed.set_thumbnail(url=self.ctx.guild.me.avatar_url)
		embed.set_footer(text=f"{offset:,} - {min(len_data, offset+self.per_page-1):,} of {len_data:,} commands.")

		for name, value in fields:
			embed.add_field(name=name, value=value, inline=False)

		return embed

	async def format_page(self, menu, entries):
		fields = []

		for entry in entries:
			fields.append((entry.brief or "No description.", syntax(entry)))

		return await self.write_page(menu, fields)


class Help(Cog):
	def __init__(self, bot):
		self.bot = bot
		self.bot.remove_command("help")
			
	async def cmd_help(self, ctx, command):
		embed = Embed(title=f"```\nHelp with {command}\n```",
					  description=syntax(command),
					  colour=discord.Colour.from_rgb(64,64,64))
		embed.add_field(name="```\nCommand description\n```", value=command.help)
		await ctx.send(embed=embed)

	@command(name="help")
	async def show_help(self, ctx, cmd: Optional[str]):
		"""Shows this message."""
		if cmd is None:
			menu = MenuPages(source=HelpMenu(ctx, list(self.bot.commands)),
							 delete_message_after=True,
							 timeout=60.0)
			await menu.start(ctx)

		elif (command := get(self.bot.commands, name=cmd)):
			await self.cmd_help(ctx, command)

		else:
			await ctx.embed(title="Error", description="[Help Error] The command you provided is invalid.")


def setup(bot):
	bot.add_cog(Help(bot))