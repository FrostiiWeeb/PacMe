import sys
import traceback
import datetime
import discord
import humanize
from discord.ext import commands
from discord.ext.commands import command
from discord.ext.commands import Cog
from utils.errors import InvalidTime, NotInDB

class ErrorEmbed(discord.Embed):
    def __init__(self, description, **kwargs):
        super().__init__(color=0x2F3136,
                         title="An error occurred!",
                         description=description,
                         timestamp=datetime.datetime.utcnow(), url="https://discord.gg/G2PekUfD59")


class Error(Cog):
    def __init__(self, bot):
        self.bot = bot

        self.bot.errors = {
            commands.MissingRequiredArgument: "Missing required argument(s): "
                                              "{error.param}",
            commands.MissingPermissions: f"Missing required permission(s).",                                            
            commands.BotMissingPermissions: "Im missing permission(s).",
            commands.NotOwner: "You don't own this bot.",
            commands.NSFWChannelRequired: "{ctx.command} is required to be "
                                          "invoked in a NSFW channel.",
            commands.MaxConcurrencyReached: "{ctx.command} is already being "
                                            "used, please wait.",
            commands.DisabledCommand: "{ctx.command} has been disabled, please wait until it's enabled.",
            commands.BadUnionArgument: "Cannot convert Argument into int, str, etc..",
            commands.ExtensionNotFound: "The extension you provided is invalid.",
            commands.ExtensionNotLoaded: "The extension you provided has not been loaded.",
            commands.BadArgument: "Bad argument, cannot convert to int, str, discord member..",  
            discord.HTTPException: None,
            commands.CommandOnCooldown: None,
            InvalidTime: "That's an invalid unit!",
            NotInDB: "That is not in the database."
        }

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.__class__.__name__} Cog has been loaded\n-----")

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):

        error = getattr(error, "original", error)
        description: str = None

        if isinstance(error, tuple(self.bot.errors.keys())):
            reinvokable = (isinstance(error, commands.MissingPermissions) and
                           await self.bot.is_owner(ctx.author))

            if reinvokable:
                return await ctx.reinvoke()
            description = str.format(self.bot.errors[type(error)],
                                     ctx=ctx,
                                     error=error)
        else:
            ignored = (commands.CommandNotFound, commands.CheckFailure,)
            if isinstance(error, ignored):
            	return 
            formatted = traceback.format_exception(
                type(error),
                error,
                error.__traceback__
            )
            description = ("").join(formatted)
            print(description, file=sys.stderr)
                        
        try:
            formatted = traceback.format_exception(
                type(error),
                error,
                error.__traceback__
            )
            await ctx.reply(embed=ErrorEmbed(description=f"```\n{description}\n```"))
        except discord.Forbidden:
            pass


def setup(bot):
    bot.add_cog(Error(bot))
