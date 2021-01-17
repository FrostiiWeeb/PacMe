import json

import discord
from discord.ext import commands


class Config(commands.Cog, name="Configuration"):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.__class__.__name__} Cog has been loaded\n-----")

    @commands.Cog.listener()
    async def on_guild_remove(self, ctx):
        with open("./prefixes.json", "r") as f:
            prefixes = json.load(f)

            prefixes.pop(str(ctx.guild.id))

            with open("./prefixes.json", "w") as f:
                json.dump(prefixes, f, indent=4)

    @commands.command(aliases=['pf'], help="Change the prefix for the server.")
    @commands.has_permissions(administrator=True)
    async def prefix(self, ctx, new_prefix):
        embed = discord.Embed(
            colour=self.bot.grey,
            title="Prefix Updated",
            description=None,
            timestamp=ctx.message.created_at
        )
        embed.add_field(name="New Prefix:", value=f"{new_prefix}", inline=True)
        embed.add_field(name="Example:", value=f"{new_prefix}help", inline=True)

        with open("./prefixes.json", "r") as f:
            prefixes = json.load(f)
            prefixes[str(ctx.guild.id)] = new_prefix

            with open("./prefixes.json", "w") as f:
                json.dump(prefixes, f, indent=4)
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Config(bot))
