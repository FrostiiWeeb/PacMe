import sys
import traceback

import discord
from discord.ext import commands
from discord.ext.commands import command
from discord.ext.commands import Cog

class Error(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        self.errors = {
            commands.MissingRequiredArgument: "Missing required argument(s): "
                                              "{error.param}",
            commands.MissingPermissions: "Missing permission(s).",
            commands.CommandNotFound: "The command you provided is invalid.",
            commands.NotOwner: "You don't own this bot.",
            commands.NSFWChannelRequired: "{ctx.command} is required to be "
                                          "invoked in a NSFW channel.",
            commands.MaxConcurrencyReached: "{ctx.command} is already being "
                                            "used, please wait.",
            commands.DisabledCommand: "{ctx.command} has been disabled, please wait until it's enabled."
        }

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.__class__.__name__} Cog has been loaded\n-----")

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        error = getattr(error, "original", error)
        description: str = None

        if isinstance(error, tuple(self.errors.keys())):
            reinvokable = (isinstance(error, commands.MissingPermissions) and
                           await self.bot.is_owner(ctx.author))

            if reinvokable:
                return await ctx.reinvoke()
            description = str.format(self.errors[type(error)],
                                     ctx=ctx,
                                     error=error)
        else:
            formatted = traceback.format_exception(
                type(error),
                error,
                error.__traceback__
            )
            description = ("").join(formatted)
            print(description, file=sys.stderr)
        await ctx.message.add_reaction('<:redTick:596576672149667840>')
        log_channel = discord.Embed(colour=discord.Colour.from_rgb(64, 64, 64), title="Error", description=f"**Error Author:** {ctx.author}\n**Error Guild:** {ctx.guild.name}\n**Main Error:** ```\n{description}\n```")
        embed = discord.Embed(
            colour=discord.Colour.from_rgb(64, 64, 64),
            description=f"```\n{description}\n```",
            title="```Error```"
        )

        try:
            channel = self.bot.get_channel(789892435190349860)
            await channel.send(embed=log_channel)
            await ctx.reply(embed=embed)
        except discord.Forbidden:
            pass


def setup(bot):
    bot.add_cog(Error(bot))
