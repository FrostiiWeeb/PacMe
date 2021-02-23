import json

import discord
from discord.ext import commands


class Config(commands.Cog, name="Configuration"):
    def __init__(self, bot):
        self.bot = bot		
       
    @commands.command(name="toggle", description="Enable or disable a command!")
    @commands.is_owner()
    async def toggle(self, ctx, *, command):
        command = self.bot.get_command(command)

        if command is None:
            await ctx.send("I can't find a command with that name!")

        elif ctx.command == command:
            await ctx.send("You cannot disable this command.")

        else:
            command.enabled = not command.enabled
            ternary = "enabled" if command.enabled else "disabled"
            await ctx.send(f"I have {ternary} {command.qualified_name} for you!")
   

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.__class__.__name__} Cog has been loaded\n-----")
    
    @commands.command(
        name="prefix",
        aliases=["changeprefix", "setprefix"],
        help="Change your guilds prefix!",
        breif="Change your guilds prefix!",
        usage="[prefix]",
    )
    @commands.has_permissions(administrator=True)
    async def prefix(self, ctx, *, prefix="!*"):
             
        await self.bot.config.upsert({"_id": ctx.guild.id, "prefix": prefix})
        self.bot.cache[ctx.guild.id] = await self.bot.config.get_by_id(ctx.guild.id)   
        await ctx.embed(description=f"**Changed prefix to:**\n{prefix}\n**Example:**\n{prefix}help")


def setup(bot):
    bot.add_cog(Config(bot))
