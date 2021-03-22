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
from discord import Member
from discord.ext.commands import Cog, Greedy
from discord.ext.commands import CheckFailure
from discord.ext.commands import command, has_permissions
import sys
import aiohttp
import json
import subprocess
from prettytable import PrettyTable
from asyncpg import UniqueViolationError
from utils.mongo import Connection

class Owner(commands.Cog, command_attrs={"hidden": True}):
    def __init__(self, bot):
        self.bot = bot 
        self.bot.session = aiohttp.ClientSession()   
        bot.add_check(self.maintenence_mode)
        



    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.__class__.__name__} Cog has been loaded\n-----")

        
    @commands.group(hidden=True,case_insensitive=True, help="Dev commands.",aliases=['d'],invoke_without_command=True, brief="Dev commands")
    @commands.is_owner()
    async def dev(self, ctx):
    	embed = discord.Embed(colour=0x2f3136, title="Hey.", description="**Dev commands:**\ndev load\ndev unload\ndev reload\ndev eval\ndev reboot\ndev m")
    	await ctx.send(embed=embed)
    	return
        	
   

    @dev.command(hidden=True,help="Load or unload cogs.",aliases=["load", "unload"], usage="<cog>")
    @commands.is_owner()
    async def manipulate(self, ctx, cog: str = None):
        if str(cog) == None:
        	if ctx.invoked_with == "reload":
        		embed = discord.Embed()
        		for c in os.listdir('.'):
        			try:
        				if c.endswith(".ttf"):
        					pass
        				if c.endswith(".jpg"):
        					pass
        				self.bot.reload_extension(f"{c[:-3]}")
        				embed.add_field(name=str(c), value=self.bot.emoji_dict["greenTick"])
        			except Exception as e:
        				embed.add_field(name=str(c), value=self.bot.emoji_dict["redTick"])                
        
        manipulate_extension = getattr(
            self.bot,
            f"{ctx.invoked_with}_extension",
            None
        )

        if ctx.invoked_with == "manipulate" or manipulate_extension is None:
            return				
        			
        manipulate_extension(f"{cog}")
        embed = Embed(description=f"{self.bot.emoji_dict['greenTick']} {ctx.invoked_with}ed {cog}", colour=0x2f3136)
        embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)    		

    @dev.command(hidden=True,help="Confirm to use maintenance mode.",aliases=['cf'])
    async def confirm(self, ctx):
	    if ctx.author.id in self.bot.owner_ids:
	        
		    self.bot.maint = True
		    embed = discord.Embed(title="Ya been confirmed to use maintenance mode!", colour=0x2f3136)	
		    await ctx.send(embed=embed)
	    else:
		    self.bot.maint = False
		    embed = discord.Embed(title="OOF, ya have not been confirmed to use maintenance mode.", colour=0x2f3136)  
		    await ctx.send(embed=embed)      
        
    @dev.command(hidden=True,help="Restart the bot.",aliases=['r', 'reboot', 'res'])
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
        			os.system('exit()')
        		
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
     
 

    @dev.command(help="Turn on or off maintenance mode.",aliases=['maintenance'], hidden=True)
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
                   	
  
     
    @dev.command(name="raw")
    async def rawmsg(self, ctx, msg_id):
     	msg = await self.bot.http.get_message(ctx.channel.id, msg_id)
     	msg = json.dumps(msg, indent=4)
     	if len(msg) > 1989:
     	    await ctx.embed(description=f"Content too long: {await self.bot.mystbin.post(msg)}")
     	    return
     	await ctx.embed(description=f"```json\n{msg}\n```")
     
    
    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
    	if isinstance(error, commands.MissingPermissions):
    		embed = discord.Embed(title="Uh..", description=f"{self.bot.errors[commands.MissingPermissions]}", colour=0x2f3136)
    		await ctx.reply(embed=embed)
    
    @dev.command(hidden=True)
    @commands.is_owner()
    async def sync(self, ctx):
    	out = subprocess.check_output("git pull", shell=True)
    	await ctx.send(f"```\n{out.decode('utf-8')}\n```")
    	await ctx.invoke(self.bot.get_command("jsk reload"))
    

    
    @dev.command(hidden=True)
    @commands.is_owner()
    async def upload(self, ctx):
    	out = subprocess.check_output("git push", shell=True)
    	await ctx.send(f"```\n{out.decode('utf-8')}\n```")   
    
    @commands.group(invoke_without_command=True) 
    @commands.is_owner()
    async def blacklist(self, ctx):
    	pass
    
    @blacklist.command()
    @commands.is_owner()
    async def add(self, ctx, user_id : int):
    	user = user_id
    	
    	try:
    		data = await self.bot.db.fetchrow("SELECT user_id FROM blacklist WHERE user_id = $1", user)
    		if data['user_id'] == user.id:
    			await ctx.embed(description="Already blacklisted thst user!")
    	except:
    		try:
    			await self.bot.db.execute("INSERT INTO blacklist(user_id) VALUES ($1)", user)
    			await ctx.embed(description=f"Blacklisted {await self.bot.fetch_user(user)}")
    		except:
    			await ctx.embed(description="That user is already blacklisted.")
    
    @blacklist.error
    async def blacklist_error(self, ctx, error):
    	if isisntace(error, UniqueViolationError):
    		await ctx.embed(description="That user is already blacklisted.")
    
    @commands.group(invoke_without_command=True)
    async def emoji(self, ctx):
    	pass
    
    @emoji.command(name="add")
    async def add(self, ctx, id : int, name: str):
    	await self.bot.db.execute(
    	"INSERT INTO emojis(id, name) VALUES ($1, $2)", id, name
    	)
    	await ctx.send("Added `{}` as an emoji.".format(name))
    	self.bot._emojis[name] = f"<:{name}:{id}>"
    	
    @dev.command()
    @commands.is_owner()
    async def sql(self, ctx, *, query):
        """Execute SQL commands"""
        res = await self.bot.db.fetch(query)
        if len(res) == 0:
            return await ctx.message.add_reaction('✅')
        headers = list(res[0].keys())
        table = PrettyTable()
        table.field_names = headers
        for record in res:
            lst = list(record)
            table.add_row(lst)
        msg = table.get_string()
        await ctx.send(f"```\n{msg}\n```")		    		    	

def setup(bot):
    bot.add_cog(Owner(bot))
