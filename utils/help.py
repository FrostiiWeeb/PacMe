from typing import Optional

import discord
from discord import Embed
from discord.utils import get
from discord.ext.menus import MenuPages, ListPageSource
from discord.ext import menus
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

def cog_cmds(ctx, cog):
	cog = ctx.bot.get_cog(cog)
	cmds = ", ".join(c.qualified_name or c.name for c in cog.get_commands())
	return cmds
	
def cog_nms(ctx, cog):
	cog = ctx.bot.get_cog(cog)
	name = cog.qualified_name
	return name

class HelpMenu(ListPageSource):
	def __init__(self, ctx, data):
		self.lmao = ctx

		super().__init__(data, per_page=2)

	async def write_page(self, menu, fields=[]):
		offset = menu.current_page * self.per_page

		embed = Embed(title="Help",
					  description=f"```\nHelp Menu ({len(self.lmao.bot.commands)} commands.)\n```")
		embed.set_thumbnail(url=self.lmao.guild.me.avatar_url)
		embed.set_footer(text = f"Page {menu.current_page+1}/5"
        if self.get_max_pages() > 0 else "Page 0/0")

		for name, value in fields:
			embed.add_field(name=name, value=value, inline=False)

		return embed

	async def format_page(self, menu, entries):
		fields = []

		for entry in entries:

			fields.append((cog_nms(self.lmao, entry), cog_cmds(self.lmao, entry)))

		return await self.write_page(menu, fields)

class GroupHelpSource(ListPageSource):
    def __init__(self, group, data):
        super().__init__(data, per_page=5)
        self.group = group

    async def format_page(self, menu, entries):
        offset = menu.current_page * self.per_page
        embed = discord.Embed(title = str(self.group),
                              color=0x36393E)

        for index, command in enumerate(entries, start=offset):
            embed.add_field(name=command.qualified_name,
                            value=(
                                f"[{' | '.join([alias for alias in command.aliases])}] \n" if command.aliases else ""
                                f"{command.help or 'None'}"
                            ))

        embed.set_footer(text=f"Page {menu.current_page + 1}/{self.get_max_pages()}" if
            self.get_max_pages() > 0 else "Page 0/0")
        return embed


class CogHelpSource(ListPageSource):
    def __init__(self, cog, data):
        super().__init__(data, per_page=6)
        self.cog = cog

    async def format_page(self, menu, entries):
        offset = menu.current_page * self.per_page
        embed = discord.Embed(title=self.cog.qualified_name)

        for index, command in enumerate(entries, start=offset):
            embed.add_field(
                name=f"**{str(command)}** [{' | '.join(alias for alias in command.aliases)}]" if command.aliases else f"**{str(command)}**",
                value=(
                    f"{command.help}" or "None"
                ), inline=False
            )

        embed.set_footer(text = f"Page {menu.current_page+1}/{self.get_max_pages()}"
        if self.get_max_pages() > 0 else "Page 0/0")

        return embed
        
class CogHelpPages(MenuPages):
    def __init__(self, source):
        super().__init__(source, delete_message_after=True, timeout=60.0)
       
def command_info(command : Union[str, commands.Command]):
       info = ""
       if command.brief:
       	info += command.brief
       if command.help:
       	info += command.description
       else:
       	info += "None"
       return info
       
async def cmd_help(ctx, command):
					  embed = Embed(title=f"Help",
					  description=syntax(command) + "\n" + command_info(command))
					  await ctx.send(embed=embed)
					  
class HelpPages(MenuPages):
	def __init__(self, source):
		super().__init__(source, delete_message_after=True, timeout=60.0)
	
	@menus.button('\U00002754', position=menus.Last(4))
	async def show_bot_help(self, payload):
		"""
		Shows the bot help message
		"""
		embed = discord.Embed(title="Bot help", description="Hello! Welcome to the bot help page.")
		embed.add_field(name="[arg]", value="Optional argument!", inline=False)
		embed.add_field(name="<arg>", value="Required argument!", inline=False)
		embed.add_field(name="What to do?", value="Use `@PacMe#9790 help [cmd]` for command help and `@PacMe#9790 help [module]` for module help.")
		await self.message.edit(content=None, embed=embed)
		
	
	@menus.button('\N{INFORMATION SOURCE}\ufe0f', position=menus.Last(3))
	async def show_help(self, payload):
	       """Shows this message"""
	       embed = discord.Embed(title='Paginator help', description='Hello! Welcome to the help page.')
	       messages = []
	       for (emoji, button) in self.buttons.items():
	       	messages.append(f'{emoji}: {button.action.__doc__}')
	       	
	       embed.add_field(name='What are these reactions for?', value='\n'.join(messages), inline=False)
	       await self.message.edit(content=None, embed=embed)					
	
class PaginatedHelp(commands.HelpCommand):
	async def send_bot_help(self, mapping):
		menu = HelpPages(source=HelpMenu(ctx=self.context, data=list(self.context.bot.cogs)))
		
		await menu.start(self.context)
	
	async def send_command_help(self, command):
		return await cmd_help(ctx=self.context, command=command)
	
	async def send_group_help(self, group: commands.Group):
	       menu = CogHelpPages(source=GroupHelpSource(group, await self.filter_commands(group.commands)))
	       await menu.start(self.context)
	
	async def send_cog_help(self, cog):
	       menu = CogHelpPages(source=CogHelpSource(cog, await self.filter_commands(cog.get_commands())))
	       await menu.start(self.context)
		     	