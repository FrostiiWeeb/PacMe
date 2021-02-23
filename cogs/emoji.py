import discord
from discord.ext import commands

class Emoji(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener("on_message")
    async def emoji(self, msg):
    	if ";" in msg.content:
    		emj_name = msg.content[1:-1]
    		for emj in msg.guild.emojis:
    			if emj_name == emj.name:
    				await msg.channel.send(str(emj))

def setup(bot):
    bot.add_cog(Emoji(bot))