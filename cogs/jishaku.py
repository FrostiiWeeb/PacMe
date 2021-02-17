import jishaku
from jishaku.cog import STANDARD_FEATURES, OPTIONAL_FEATURES
from jishaku.features.baseclass import Feature
from discord.ext import commands


class jishaku(*OPTIONAL_FEATURES, *STANDARD_FEATURES):
    @Feature.Command(name="jishaku", aliases=["jsk"], invoke_without_command=True, ignore_extra=False)
    async def jsk(self, ctx: commands.Context):
    	await ctx.send("I'm walking on a Star!")
    @Feature.Command(parent="jsk", name="foobar")
    async def jsk_foobar(self, ctx: commands.Context):
        await ctx.send("Hello there!")
        
def setup(bot: commands.Bot):
    bot.add_cog(jishaku(bot=bot))       
