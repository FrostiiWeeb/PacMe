import discord
from discord.ext import commands
from discord.ext import paginator
from typing import Union
import random

class Games(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		self.questions = {"What is my name?": "PacMe", "What is my owner name?": "FrostiiWeeb"}
		
	@commands.command()
	async def quiz(self, ctx):
		for i in self.questions:
			await ctx.author.send(i)
		try:
			def check(m):
				return m.author == ctx.author and m.author != ctx.bot.user
			msg = await self.bot.wait_for("message", check=check)
			if msg.content == self.questions["What is my name?"]:
				await ctx.author.send("Correct!")
			if msg.content == self.questions["What is my owner name?"]:
				await ctx.author.send("Correct!")
		except Exception as e:
			print(e)
			return
			

def setup(bot):
	bot.add_cog(Games(bot))