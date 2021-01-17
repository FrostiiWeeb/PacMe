from discord.ext import commands
import ast
import platform
import discord
from discord import Embed
import os
import asyncio
import sys
import psutil
import contextlib
from disputils import BotEmbedPaginator, BotConfirmation, BotMultipleChoice
import textwrap
import traceback
from traceback import format_exception


class Owner(commands.Cog, command_attrs={"hidden": True}):
    def __init__(self, bot):
        self.bot = bot
        bot.add_check(self.maintenence_mode)


    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.__class__.__name__} Cog has been loaded\n-----")
        
    @commands.group(case_insensitive=True, help="Dev commands.",aliases=['d'],invoke_without_command=True)
    @commands.is_owner()
    async def dev(self, ctx):
    	embed = discord.Embed(colour=self.bot.grey, title="Hey.", description="**Dev commands:**\ndev load\ndev unload\ndev reload\ndev eval\ndev reboot\ndev m")
    	await ctx.send(embed=embed)
    	return
   

    @dev.command(help="Load or unload cogs.",aliases=["load", "unload"])
    @commands.is_owner()
    async def manipulate(self, ctx, *, cog: str):
        manipulate_extension = getattr(
            self.bot,
            f"{ctx.invoked_with}_extension",
            None
        )

        if ctx.invoked_with == "manipulate" or manipulate_extension is None:
            return
        manipulate_extension(f"cogs.{cog}")
        embed = Embed(title=f"Succesfully {ctx.invoked_with}ed {cog}", description=f"{ctx.invoked_with}ed {cog}", colour=self.bot.grey)
        embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)    		

    @dev.command(help="Confirm to use maintenance mode.",aliases=['cf'])
    async def confirm(self, ctx):
	    if ctx.author.id in self.bot.owner_ids:
		    self.bot.maint = True
		    embed = discord.Embed(title="Ya been confirmed to use maintenance mode!", colour=self.bot.grey)	
		    await ctx.send(embed=embed)
	    else:
		    self.bot.maint = False
		    embed = discord.Embed(title="OOF, ya have not been confirmed to use maintenance mode.", colour=self.bot.grey)  
		    await ctx.send(embed=embed)      
        
    @dev.command(help="Restart the bot.",aliases=['r', 'reboot', 'res'])
    @commands.is_owner()
    async def restart(self, ctx):
        embed = discord.Embed(title="Are you sure you want to restart?", colour=discord.Colour.blurple())
        embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
        confirmed = discord.Embed(title="Alright, imma be back in a few secs!", colour=discord.Colour.green())
        confirmed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
        notc = discord.Embed(title="Aight, imma be here if ya need me!", colour=self.bot.colour)
        notc.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
        mssg = await ctx.send(embed=embed)
        await mssg.add_reaction('✅')
        await mssg.add_reaction('❌')
        
        def check(reaction, user):
        	return user == ctx.author and str(reaction.emoji) in ["✅", "❌"]
        	
        while True:
        	try:
        		reaction, user = await self.bot.wait_for("reaction_add", timeout=60.5, check=check)
        		
        		if str(reaction.emoji) == "✅":
        			await mssg.edit(embed=confirmed)
        			await asyncio.sleep(1.5)
        			await ctx.bot.logout()
        		
        		elif str(reaction.emoji) == "❌":
        			await mssg.edit(embed=notc)
        			break
        			return
        	except asyncio.TimeoutError:
        		await mssg.delete()
        		return
    
            
    async def maintenence_mode(self, ctx):
        if self.bot.maintenence:
        	if ctx.author.id in self.bot.owner_ids:
        		self.bot.maint = True
        	else:
        	    embed = discord.Embed(description="Sorry, but maintenence mode is active.",colour=discord.Colour(0xffff00))
        	    embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
        	    await ctx.send(embed=embed, delete_after=60)        		
        	    
        	    return False
        	
        return True
 

    @dev.command(help="Turn on or off maintenance mode.",aliases=['maintenance'])
    @commands.is_owner()
    async def m(self, ctx):
        if self.bot.maint == True:
            if self.bot.maintenence:
               self.bot.maintenence = False
               await ctx.send("Maintenance is now off.")
            else:
               if self.bot.maint == True:
                   self.bot.maintenence = True
                   await ctx.send("Maintenance is now on.")
        else:
        	pass
        	
    @dev.command(aliases=['rl'], help="Reload all/specific cog.")
    @commands.is_owner()
    async def reload(self, ctx, cog=None):
        if not cog:
            # No cog, means we reload all cogs
            async with ctx.typing():
                embed = discord.Embed(
                    title="Reloading all cogs!",
                    color=0x808080,
                    timestamp=ctx.message.created_at
                )
                for ext in os.listdir("./cogs/"):
                    if ext.endswith(".py") and not ext.startswith("_"):
                        try:
                            self.bot.unload_extension(f"cogs.{ext[:-3]}")
                            self.bot.load_extension(f"cogs.{ext[:-3]}")
                            embed.add_field(
                                name=f"Reloaded: `{ext}`",
                                value='\uFEFF',
                                inline=False
                            )
                        except Exception as e:
                            embed.add_field(
                                name=f"Failed to reload: `{ext}`",
                                value=e,
                                inline=False
                            )
                        await asyncio.sleep(0.5)
                await ctx.send(embed=embed)
        else:
            # reload the specific cog
            async with ctx.typing():
                embed = discord.Embed(
                    title=f"Reloading {cog}!",
                    color=0x808080,
                    timestamp=ctx.message.created_at
                )
                ext = f"{cog.lower()}.py"
                if not os.path.exists(f"./cogs/{ext}"):
                    # if the file does not exist
                    embed.add_field(
                        name=f"Failed to reload: `{ext}`",
                        value="This cog does not exist.",
                        inline=False
                    )

                elif ext.endswith(".py") and not ext.startswith("_"):
                    try:
                        self.bot.unload_extension(f"cogs.{ext[:-3]}")
                        self.bot.load_extension(f"cogs.{ext[:-3]}")
                        embed.add_field(
                            name=f"Reloaded: `{ext}`",
                            value='\uFEFF',
                            inline=False
                        )
                    except Exception:
                        desired_trace = traceback.format_exc()
                        embed.add_field(
                            name=f"Failed to reload: `{ext}`",
                            value=desired_trace,
                            inline=False
                        )
                await ctx.send(embed=embed)

    
    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
    	if isinstance(error, commands.MissingPermissions):
    		embed = discord.Embed(title="```Error```", description=f"```\nMissing permission(s).\n```", colour=discord.Colour.from_rgb(64, 64, 64))
    		await ctx.reply(embed=embed)

def setup(bot):
    bot.add_cog(Owner(bot))
