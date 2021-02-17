import discord
from discord.ext import commands
from datetime import datetime
from pathlib import Path

class PacContext(commands.Context):
	
	async def send_reply(self, content=None, embed=None, mention_author=False):
		if content is None:
			await self.reply(embed=embed, mention_author=mention_author)
			return
		await self.reply(content, mention_author=False)
		

	
	async def embed(self, *args, **kwargs):
	       """Sends an embed with the args given"""
	       embed = discord.Embed(**kwargs, color=0x2F3136, timestamp=datetime.utcnow()).set_author(name=f"{self.author}", icon_url=str(self.author.avatar_url))
	       await self.send(embed = embed)