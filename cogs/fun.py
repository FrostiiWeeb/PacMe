import asyncio
import random
import time
import aiohttp
import discord
import re
from discord.ext import commands
from datetime import datetime
import wikipedia
import requests
from PIL import Image, ImageDraw, ImageFont, ImageFont
import textwrap
import mystbin
from io import BytesIO
import json
from owotext import OwO
import aiozaneapi
from typing import Union
import asyncpraw as praw

def get_embed(_title, _description, _color):
    return discord.Embed(title=_title, description=_description, color=_color)


class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.r = praw.Reddit(client_id= "4DS49vhbKM7Z0A",
     client_secret = "y0q6O6ApzmPxAER3MfkjEkwiScHI9Q",
     username="FrostiiWeeb",
     password="iamreddit",
     user_agent="FrostiiA")
        self.timeouts = [20, 25, 30, 40, 45, 50, 55, 60]   

        
    
        
    @commands.command()
    async def jpeg(self, ctx, user: Union[discord.Member, int] = None):
        user = user or ctx.author
        img = await self.bot.zane.jpeg(str(user.avatar_url))
        f = discord.File(img, "jpeg.gif")
        embed = discord.Embed(color=self.bot.grey).set_image(url="attachment://jpeg.gif")
        await ctx.send(embed = embed,file=f)         

    @commands.command()
    async def braille(self, ctx, user: Union[discord.Member, int] = None):
        user = user or ctx.author
        img = await self.bot.zane.braille(str(user.avatar_url))
        f = discord.File(img, "braille.gif")
        embed = discord.Embed(color=self.bot.grey).set_image(url="attachment://braille.gif")
        await ctx.send(embed = embed,file=f) 

    @commands.command()
    async def deepfry(self, ctx, user: Union[discord.Member, int] = None):
        user = user or ctx.author
        img = await self.bot.zane.deepfry(str(user.avatar_url))
        f = discord.File(img, "deepfry.gif")
        embed = discord.Embed(color=self.bot.grey).set_image(url="attachment://deepfry.gif")
        await ctx.send(embed = embed,file=f)          
                        
    @commands.command()
    async def spread(self, ctx, user: Union[discord.Member, int] = None):
        user = user or ctx.author
        img = await self.bot.zane.spread(str(user.avatar_url))
        f = discord.File(img, "spread.gif")
        embed = discord.Embed(color=self.bot.grey).set_image(url="attachment://spread.gif")
        await ctx.send(embed = embed,file=f)         
        
    @commands.command()
    async def dots(self, ctx, user: Union[discord.Member, int] = None):
    	user = user or ctx.author
    	img = await self.bot.zane.dots(str(user.avatar_url))  
    	f = discord.File(img, "dots.gif")   
    	embed = discord.Embed(color=self.bot.grey).set_image(url="attachment://dots.gif") 
    	await ctx.send(embed = embed,file=f)     	
    
        
    @commands.command()
    async def floor(self, ctx, user: Union[discord.Member, int] = None):
    	user = user or ctx.author
    	img = await self.bot.zane.floor(str(user.avatar_url))  
    	f = discord.File(img, "floor.gif")
    	embed = discord.Embed(color=self.bot.grey).set_image(url="attachment://floor.gif") 
    	await ctx.send(embed = embed,file=f)
    	
    @commands.command()
    async def magik(self, ctx, user: Union[discord.Member, int] = None):
     user = user or ctx.author
     img = await self.bot.zane.magic(str(user.avatar_url))
     f = discord.File(img, "magik.gif")     
     embed = discord.Embed(color=self.bot.grey).set_image(url="attachment://magik.gif")
     await ctx.send(embed=embed,file=f)
     
     
    @commands.command(name="8ball", brief="Ask the 8ball something and itll answer!", help="Ask the 8ball something.")
    async def _8ball(self, ctx, *, question):
            if question == "Are you gay?":
            	await ctx.embed(description=f"Question: Are you gay?\nAnswer: **gulps** Uhm, definetly not!")
            	return
            responses = [
            "It is certain.",
            "It is decidedly so.",
            "Without a doubt.",
            "Yes - definitely.",
            "You may rely on it.",
            "As I see it, yes.",
            "Most likely.",
            "Outlook good.",
            "Yes.",
            "Signs point to yes.",
            "Reply hazy, try again.",
            "Ask again later.",
            "Better not tell you now.",
            "Cannot predict now.",
            "Concentrate and ask again.",
            "Don't count on it.",
            "My reply is no.",
            "My sources say no.",
            "Outlook not so good.",
            "Very doubtful."]
            await ctx.embed(description=f'Question: {question}\nAnswer: {random.choice(responses)}')

    		      
    @commands.Cog.listener()
    async def on_ready(self):
    	print(f"{self.__class__.__name__} Cog has been loaded\n-----")
    	
    @commands.command(help="Draw text you want!", breif="Draw the text ya want!")
    async def text(self, ctx, *, text="Hi"):
    	offset = margin = 10
    	img = Image.open('/storage/emulated/0/discord/cogs/pure-black-background-f82588d3.jpg')
    	draw = ImageDraw.Draw(img)
    	font = ImageFont.truetype('/storage/emulated/0/discord/cogs/Minecraftia.ttf', 47)
    	textwrapped = textwrap.wrap(text, width=34)
    	draw.text((offset,margin), '\n'.join(textwrapped), (255,255,255), font=font)
    	
    	img.save("test.png")
    	await ctx.send(file = discord.File("test.png"))
    	
    @commands.command()
    async def paste(self, ctx, *, paste):
    	paste = await self.bot.mystbin.post(paste, syntax="python")
    	await ctx.send(str(paste))
   	

    @commands.command(help="Enlarge a emoji!", brief="Enlarge a emoji!")
    async def enlarge(self, ctx, emoji: discord.PartialEmoji = None):
        if not emoji:
            await ctx.embed(title="You need to provide an emoji!")
        else:
            await ctx.send(emoji.url)
            
    	
    @commands.command(brief="Get wiki!", help="idk")
    async def wiki(self,ctx,*,word):
        def viki_sum(arg):
            definition = wikipedia.summary(arg,sentences=3,chars=2047)
            return definition
        embed = discord.Embed(title=f"Got the wiki of {word}!",description=f"**{viki_sum(word)}**")
        await ctx.send(embed=embed)


    @commands.command(aliases=['c'], help="Grab the cookie!", brief="Get the cookie!")
    @commands.max_concurrency(1, per=commands.BucketType.channel, wait=False)
    async def cookie(self, ctx):
    	embedm = discord.Embed(title="Grab the :cookie:!", description="3")
    	embed1 = discord.Embed(title="Grab the :cookie:!", description="2")
    	embed2 = discord.Embed(title="Grab the :cookie:!", description="1")
    	embedg = discord.Embed(title="Grab the :cookie:!", description="Go!")
    	add_reaction = '🍪'
    	msg = await ctx.send(embed=embedm)
    	await asyncio.sleep(1)
    	await msg.edit(embed=embed1)
    	await asyncio.sleep(1)
    	await msg.edit(embed=embed2)
    	await asyncio.sleep(1)
    	await msg.edit(embed=embedg)
    	def check(reaction, user):
    		return str(reaction.emoji) == add_reaction and not user == self.bot.user and not user.bot
    	try:
    		startt = time.time()
    		await msg.add_reaction(add_reaction)
    		reaction, user = await self.bot.wait_for('reaction_add', check=check, timeout=15.0)
    		endd = time.time()
    		emb = discord.Embed(title="Mmm", description=f"{user} Got the :cookie: in `{round(endd - startt, 2)}` seconds!")
    		await msg.edit(embed=emb)
    		
    	except asyncio.TimeoutError:
    		noonewon = discord.Embed(title=":c", description="Nobody got the :cookie:..")
    		await msg.edit(embed=noonewon)
    		
    @commands.command(brief="Play a game of typeracer!",help="Play a game of typeracer!",aliases=['tr', 'typeracer'])
    @commands.max_concurrency(1, per=commands.BucketType.channel, wait=False)
    async def type(self, ctx):
        offset = margin = 10        
        text = await aiohttp.ClientSession().get(url='https://type.fit/api/quotes')
            
        text = json.loads(await text.read())
        text = random.choice(text)
        author = text['author']
        text = text['text']
        img = Image.open('/storage/emulated/0/discord/cogs/pure-black-background-f82588d3.jpg')
        draw = ImageDraw.Draw(img)
        font = ImageFont.truetype('/storage/emulated/0/discord/cogs/RobotoMono-Bold.ttf', 47)
        textwrapped = textwrap.wrap(text, width=34)
        draw.text((offset,margin), '\n'.join(textwrapped), (255,255,255), font=font)
        obj = BytesIO()
        img.save(obj, 'PNG')
        obj.seek(0)
        f = discord.File(obj, filename="type.png")
        timeout = random.choice(self.timeouts)
        embed = discord.Embed(
            title="```Typeracer!```",
            description=f'```\nYou have {timeout} seconds to type:```',
            color=self.bot.grey
        )
        embed.set_image(url="attachment://type.png")
        embed.set_footer(text=f"- {author}")
        await ctx.send(file=f, embed=embed)

        def is_correct(msg):
            # prevent all bots from partaking - prevents auto-cheating
            return (msg.content.startswith(f'{text}') and not msg.author.bot)

        start = time.time()  # start timer once quote is sent

        try:
            guess = await self.bot.wait_for("message",
                                            check=is_correct,
                                            timeout=timeout)
        except asyncio.TimeoutError:
                                  await ctx.embed(title="```GG.```",
                                  description="```\nYou guys took so much time smh!\n```")
        else:
            if guess.content == text:
                end = time.time()
                diff = end - start
                await ctx.embed(
                title="```Hi.```",
                description=f"```\n{guess.author} got it, and took:```\n```{round(diff)} seconds.```")
     
    @commands.command()
    async def reddit(self, ctx, sub_r = None):
     reddit = self.r
     try:
     	subr = await reddit.subreddit(sub_r)
     	all_subs = []
     	top = subr.top(limit=200)
     	async for sub in top:
     		all_subs.append(sub)
     	
     	random_sub = random.choice(all_subs)
     	name = random_sub.title
     	url = random_sub.url
     	
     	embed = discord.Embed(color=self.bot.grey, title=name).set_image(url=url)
     	await ctx.send_reply(embed=embed)
     	
     except AttributeError:
     	pass        	

    @commands.command(brief="Get some juicy memes!",help="Get some memes mate.",aliases=['memes'])
    async def meme(self, ctx):
     reddit = self.r
     try:
     	subr = await reddit.subreddit("memes")
     	all_subs = []
     	top = subr.hot(limit=50)
     	async for sub in top:
     		all_subs.append(sub)
     	
     	random_sub = random.choice(all_subs)
     	name = random_sub.title
     	url = random_sub.url
     	
     	embed = discord.Embed(color=self.bot.grey, title=name).set_image(url=url)
     	await ctx.send_reply(embed=embed)
     except AttributeError:
     	pass

def setup(bot):
    bot.add_cog(Fun(bot))
