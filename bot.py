# We import our modules.

import json
import os
from datetime import datetime
from itertools import cycle
import discord
import logging
from discord.ext import commands, tasks
from pathlib import Path
from discord.ext.commands import Bot
import inspect
import asyncio
import os
import psutil
import humanize
from utils.CustomContext import PacContext
import utils.json_loader



# Shows the current working directory.

cwd = Path(__file__).parents[0]
cwd = str(cwd)
print(f"{cwd}\n-----\nBot Type: commands.Bot\n-----")

# Define our default prefix.

default_prefix = "!*"

# Gets the prefix for the bot.

async def get_prefix(bot, message:discord.Message):
	if not message.guild:
		return commands.when_mentioned(bot,message)
		
	with open('./prefixes.json', 'r') as f:
		prefixes = json.load(f)
		
	return prefixes.get(str(message.guild.id), default_prefix)


# Makes a class for the colours.
	

class Colors:
    default = 0
    teal = 0x1abc9c
    dark_teal = 0x11806a
    green = 0x2ecc71
    dark_green = 0x1f8b4c
    blue = 0x3498db
    dark_blue = 0x206694
    purple = 0x9b59b6
    dark_purple = 0x71368a
    magenta = 0xe91e63
    dark_magenta = 0xad1457
    gold = 0xf1c40f
    dark_gold = 0xc27c0e
    orange = 0xe67e22
    dark_orange = 0xa84300
    red = 0xe74c3c
    dark_red = 0x992d22
    lighter_grey = 0x95a5a6
    dark_grey = 0x607d8b
    light_grey = 0x979c9f
    darker_grey = 0x546e7a
    blurple = 0x7289da    
		

secret_file = utils.json_loader.read_json("secrets")
class Bot(Bot):
	def __init__(self, command_prefix, **kwargs):
		super().__init__(command_prefix, **kwargs)
		self.description = "A multi-purpose bot with Fun commands, Moderation, and more!"
		self.config_token = secret_file['token']
		self.example_embed = discord.Embed(title="```Title```", description=f"```Description```", colour=discord.Colour.from_rgb(64, 64, 64))
		self.launch_time = datetime.utcnow()
		self.owner_ids = {746807014658801704, 668906205799907348}
		self.version = "1.1.3"
		self.colour = discord.Colour.red()
		self.maintenence = False
		self.maint = False
		self.colors = Colors
		self.colours = self.colors
		self.log_channel = self.get_channel(789892435190349859)
		self.loop.create_task(handle_display())
		self.loop.create_task(self.status())
		self.load_extension('jishaku')
		self.grey = discord.Colour.from_rgb(64,64,64)
		self.cwd = cwd+"/bot.py"
			
		
	async def on_message(self, message):
	       ctx = await self.get_context(message, cls=PacContext)
	       
	       await self.invoke(ctx)	     
	async def status(self):
			await bot.wait_until_ready()
			activities = cycle(["{length} servers! | !*help"])
			length = len(bot.guilds)
			name = str.format(next(activities), length=length)
			while not bot.is_closed():
				await bot.change_presence(activity=discord.Game(name=name))
				await asyncio.sleep(80) 
				
	async def on_ready(self):
	       pass
	       
display_messages = (
    ("Bot is now online!", ""),
    ("Logged in as:", "{bot.user}"),
    ("ID:", "{bot.user.id}"),
    ("Working on:", "{length} servers!"),
    ("My prefix is:", default_prefix),
    ("Discord.py version:", discord.__version__),
    ("Bot version:", "1.1.3")
)


async def handle_display():
    await bot.wait_until_ready()
    # DEV: there were 30 spaces originally
    width, _ = os.get_terminal_size()
    border = "=" * width
    output = border.center(width)
    kwargs = {
        "bot": bot,
        "length": len(bot.guilds),
        "discord": discord
    }

    for group in display_messages:
        for i, message in enumerate(group):
            message = message.format(**kwargs)
            centered = message.center(width)
            end = "\n" if i == 0 else "\n\n"
            output += centered + end
    output += border.center(width)
    print(output)

# running the bot.

if __name__ == '__main__':
	bot = Bot(command_prefix=get_prefix, intents=discord.Intents.all(), case_insensitive=True, fetch_offline_members=True, allowed_mentions=discord.AllowedMentions(roles=False, users=True, everyone=False, replied_user=False))
	for file in os.listdir(cwd+"/cogs"):
		if file.endswith(".py") and not file.startswith('_'):
			bot.load_extension(f"cogs.{file[:-3]}")
	bot.run(bot.config_token, bot=True)