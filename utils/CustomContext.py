import discord
from discord.ext import commands
from datetime import datetime
from pathlib import Path

class PacContext(commands.Context):
		
	async def embed(self, *args, **kwargs):
	       """Sends an embed with the args given"""
	       title = kwargs.get('title')
	       description = kwargs.get('description')
	       color = kwargs.get('color', 0x2F3136)
	       timestamp = kwargs.get('timestamp', datetime.utcnow())
	       url = kwargs.get("url", None)
	       embed = discord.Embed(title=title, description=description, color=color, timestamp=timestamp, url=url).set_author(name=f"{self.author}", icon_url=str(self.author.avatar_url))
	       await self.send(embed=embed)

	
	async def send_reply(self, content=None, embed=None, mention_author=False):
		if content is None:
			await self.reply(embed=embed, mention_author=mention_author)
			return
		await self.reply(content, mention_author=False)
	
	async def confirm(self, confirm_msg="Default msg."):
		embed = discord.Embed(title="Are you sure?", description=confirm_msg, color=0x2F3136)
		m = await self.send(embed=embed)
		await m.add_reaction(self.bot.emoji_dict["greenTick"])
		await m.add_reaction(self.bot.emoji_dict["redTick"])
		def check(reaction, user):
			return user == self.author and str(reaction.emoji) in [self.bot.emoji_dict["greenTick"], self.bot.emoji_dict["redTick"]]
		try:
			reaction, user = await self.bot.wait_for("reaction_add", timeout=10.5, check=check)
			if str(reaction.emoji) == self.bot.emoji_dict['greenTick']:
				c = discord.Embed(title="Aight!", description=f'{confirm_msg} -> Alright {self.author}!', color=discord.Color.green())
				await m.edit(embed=c)
			else:
				n = discord.Embed(title="Aight!", description=f'{confirm_msg} -> Alright {self.author}!', color=discord.Color.red())
				await m.edit(embed=n)
		except:
			await self.send("Ya took too long")