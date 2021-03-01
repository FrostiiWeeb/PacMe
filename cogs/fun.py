import discord
from PIL import Image, ImageDraw, ImageFont
from discord.ext import commands
import json
import aiohttp
import textwrap
import time
from wonderwords import RandomSentence
from io import BytesIO

class Fun(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		self.bot.session = aiohttp.ClientSession()
	
	@discord.ext.commands.command(aliases=['tr'])
	async def typeracer(self, ctx):
		margin = offset = 40
		text = RandomSentence()
		text = text.sentence()
		img = Image.open('/storage/emulated/0/PacMe/cogs/pure-black-background-f82588d3.jpg')
		draw = ImageDraw.Draw(img)
		font = ImageFont.truetype('/storage/emulated/0/PacMe/cogs/Minecraftia.ttf', 47)
		textwrapped = textwrap.wrap(text, width=34)
		draw.text((offset,margin), '\n'.join(textwrapped), (255,255,255), font=font)
		obj = BytesIO()
		img.save(obj, 'PNG')
		obj.seek(0)
		
		embed = discord.Embed(title="Typeracer!", description="You have `1 minute` to type:")
		f = discord.File(obj, filename="type.png")
		embed.set_image(url="attachment://type.png")
		try:

	    

		      		
		      		start = time.perf_counter()
		      		type = await self.bot.wait_for("message", timeout=60.0)
		      		await ctx.send(file=f, embed=embed)		      		
		      		if type.content == text:
		      			end = time.perf_counter()
		      			await ctx.embed(description=f"{type.author} won, and took: {round(start - end, 2)}.")
		      			
		except asyncio.TimeoutError:
			await ctx.embed(description="All of you lost lmao")
		
def setup(bot):
	bot.add_cog(Fun(bot))