import asyncio
import random
import time
import aiohttp
import discord
import re
from discord.ext import commands


class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        self.timeouts = [12.0, 19.0, 22.0]
        self.quotes = [
            "The greatest glory in living lies not in never falling, but in "
            "rising every time we fall.",
            "The way to get started is to quit talking and begin doing.",
            "Your time is limited, so don't waste it living someone else's "
            "life.",
            "If life were predictable it would cease to be life, and be "
            "without flavor.",
            "If you dont like the road your walking on, be thankful there's a "
            "road.",
            "If there's a thing I've learned in my life it's to not be afraid "
            "of the responsibility that comes with caring for other people.",
            "Help someone, you earn a friend.",
            "Your sacred space is where you can find yourself over and over "
            "again.",
            "Good times & crazy make friends the best memories.",
            "A best friend is someone who loves you when you forget to love "
            "yourself.",
            "Discord.py is a API, you can make discord bot's, and makes best "
            "freinds impressed.",
            "Everybody is a genius. But if you judge a fish by its ability to "
            "climb a tree it will live its whole life believing that it is "
            "stupid.",
            "Believing a rumor is for dummies, if you are smart, research the "
            "internet first.",
            "Making a discord bot is hard, but you'll always make it at the "
            "end.",
            "Your life has a reason, everybody's does. Don't feel down.",
            "I love those random memories that make me smile no matter what's "
            "going on in my life right now.",
            "Spelling is what we speak, what we type.",
            "What you spell, what you speak."
        ]    		
    
    @commands.command(brief="Play a game of typeracer!",help="Play a game of typeracer!",aliases=['tr', 'typeracer'])
    @commands.max_concurrency(1, per=commands.BucketType.channel, wait=False)
    async def type(self, ctx):
        quote = f'"{random.choice(self.quotes)}"'
        timeout = random.choice(self.timeouts)
        embed = discord.Embed(
            title="```Typeracer!```",
            description=f'```\nYou have {timeout} to type:\n{quote}\n```',
            color=discord.Color.from_rgb(64, 64, 64)
        )

        def is_correct(msg):
            # prevent all bots from partaking - prevents auto-cheating
            return (msg.content.startswith('"') and
                    msg.content.endswith('."') and
                    not msg.author.bot)

        await ctx.send(embed=embed)
        start = time.time()  # start timer once quote is sent
        embed = discord.Embed(title="```LOOL```",
                              description="```\nImagine cheating..\n```",
                              color=discord.Color.from_rgb(64, 64, 64))

        try:
            guess = await self.bot.wait_for("message",
                                            check=is_correct,
                                            timeout=timeout)
        except asyncio.TimeoutError:
            embed = discord.Embed(title="```GG.```",
                                  description="```\nYou guys took so much time smh!\n```",
                                  color=discord.Color.from_rgb(64, 64, 64))
            await ctx.send(embed=embed)
        else:
            if guess.content == quote:
                print("In")
                end = time.time()
                diff = end - start

                if diff >= 8:
                    print("In")
                    embed = discord.Embed(
                        title="```Hi.```",
                        description=f"```\n{guess.author} got it, and took:```\n"
                                    f"```\n{round(diff)} seconds.\n```",
                        color=discord.Color.from_rgb(64, 64, 64)
                    )
            await ctx.send(embed=embed)

    @commands.command(brief="Get some juicy memes!",help="Get some memes mate.",aliases=['memes'])
    async def meme(self, ctx):
     choices = ["A meme", "Wow such a Meme", "Bad Meme -_-", "Get lost Meme is Bad", "Bruh.. BAD MEME", "Um A Meme!", "idk what to say, this meme is SUPER", "you are a gay, this meme is gay", "Wow i love dis meme.. IM GAY", "Nope, I dont like dis meme", "Your Drunk Boi", "404 error meme bad", "Doofie Trunk would be Proud of this..", "Wow My mom will be happy after dis", "Umm UH Meme Good", "I dont understand dis meme..", "Get Lost Man.", "NoNo dont touch me there Nono My NoNo square.", "Ugh Meme Is NoNo square", "Idk lol.", "EA is going too far man..", "Memes Are the Best thing To be found..", "I dont understand, why do you like dis meme?", "Yeah yeah, soke it up.", "I cant imagine the Json File tho", "Cogs are the best right? right? RIGHT?", "Hi, would you like some coffee?", "Hi welcome to the meme town, would you like a meme?"]
     meme = random.choice(choices)
     embed = discord.Embed(color=discord.Colour.from_rgb(64,64,64), title=meme, description=None)
     async with aiohttp.ClientSession() as cs:
             async with cs.get('https://www.reddit.com/r/memes/new.json?sort=hot') as r:
             	res = await r.json()
             	embed.set_image(url=res['data']['children'] [random.randint(0, 25)]['data']['url'])
             	await ctx.send(embed=embed) 

def setup(bot):
    bot.add_cog(Fun(bot))
