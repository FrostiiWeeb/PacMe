import discord
from discord.ext import commands
from datetime import datetime
from pathlib import Path

class PacContext(commands.Context):

    async def embed(self, *args, **kwargs):
        """Sends an embed with the args given"""
        embed = discord.Embed(**kwargs, color=discord.Color.from_rgb(64, 64, 64), timestamp=datetime.utcnow())
        embed.set_footer(icon_url=str(self.author.avatar_url), text=f"Requested by {self.author}")
        await self.send(embed = embed)
        
    async def codeblock(self, ctx, text):
    	pass
