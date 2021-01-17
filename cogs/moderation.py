import asyncio
import random
from typing import Union

import discord
from discord.ext import commands


class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        self._giveaways = []
        self.muted_perms = discord.Permissions(send_messages=False, speak=False)

    def cog_unload(self):
        for task in self._giveaways:
            task.cancel()

    async def _get_mute_role(self, guild: discord.Guild):
        # automate retrieval and possible instantiation of muted role
        mute_role = discord.utils.get(guild.roles, name="Muted")

        if not mute_role:
            mute_role = await guild.create_role(
                name="Muted",
                permissions=self.muted_perms
            )
        return mute_role

    async def _do_giveaway(self,
                           ctx: commands.Context,
                           seconds: int,
                           prize: str):
        winner = None
        fields = {
            "Prize": prize,
            "Hosted by": ctx.author.mention,
            "Ends in": f"{seconds}s"
        }
        embed = discord.Embed(
            title="🎉 __New Giveaway!__ 🎉",
            colour=discord.Color.green(),
            description="React To 🎉 To Enter The Giveaway!"
        )

        for name, value in fields.items():
            embed.add_field(name=name, value=value, inline=False)
        embed.set_thumbnail(url=ctx.author.avatar_url)

        msg = await ctx.send(embed=embed)
        await msg.add_reaction("🎉")
        await asyncio.sleep(seconds)

        reaction = discord.utils.find(lambda r: str(r.emoji) == "🎉",
                                      msg.reactions)
        users = await reaction.users().flatten()
        users.remove(self.bot.user)
        winner = random.choice(users)

        embed = discord.Embed(
            title="Giveaway ended!",
            colour=discord.Colour.green(),
            description=f"Prize: {prize}\nWinner: {winner}"
        )
        await msg.edit(embed=embed)

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.__class__.__name__} Cog has been loaded\n-----")

    @commands.command(help="Ban a member!",aliases=['b'])
    @commands.has_permissions(ban_members=True)
    async def ban(self,
                  ctx,
                  member: Union[discord.Member, int], *,
                  reason="Reason not provided."):
        fields = {
            "Banned by": ctx.author,
            "Reason": reason,
            "Member banned": member
        }
        embed = discord.Embed(
            colour=discord.Colour.blurple(),
            title="__New Ban__"
        )

        for name, value in fields.items():
            embed.add_field(name=f"**{name}**:", value=value, inline=False)

        if isinstance(member, discord.Member):
            try:
                await ctx.guild.ban(member)
                await ctx.send(embed=embed)
                await member.send(embed=embed)
            except commands.MissingPermissions:
                pass
        else:
            member = discord.Object(member)
        await ctx.guild.ban(member)
        await ctx.send(embed=embed)

    @commands.command(help="Unban a member with their ID.",aliases=['ub'])
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, member_id: int):
        user = self.bot.get_user(member_id)
        title = f"Unbanned {user}"

        if user is None:
            title = f"Unbanned user with ID {member_id}"
        embed = discord.Embed(
            colour=discord.Colour.red(),
            title=title
        )

        await ctx.guild.unban(discord.Object(member_id))
        await ctx.send(embed=embed)

    @commands.command(help="Kick a member.",aliases=['k'])
    @commands.has_permissions(kick_members=True)
    async def kick(self,
                   ctx,
                   member: discord.Member, *,
                   reason="Reason not provided."):
        fields = {
            "Kicked by": ctx.author,
            "Reason": reason,
            "Member kicked": member
        }
        embed = discord.Embed(
            colour=discord.Colour.blurple(),
            title="__New Kick__"
        )

        for name, value in fields.items():
            embed.add_field(name=f"**{name}**:", value=value, inline=False)
        await member.kick(reason=reason)
        await ctx.send(embed=embed)

    @commands.command(help="Clear messages.",aliases=['c'])
    async def clear(self, ctx, amount: int = 2):
        embed = discord.Embed(
            colour=discord.Colour.green(),
            title="\u2800",
            description=f"Cleared {amount} messages!"
        )

        await ctx.channel.purge(limit=amount)
        await asyncio.sleep(1)
        msg = await ctx.send(embed=embed)
        await asyncio.sleep(2)
        await msg.delete()        
        return

    @commands.command(help="Mute a member.",aliases=['m'])
    @commands.has_permissions(kick_members=True)
    async def mute(self,
                   ctx,
                   member: discord.Member, *,
                   reason="Reason not provided."):
        embed = discord.Embed(
            colour=discord.Colour.blue(),
            title="__New Mute__"
        )
        embed.add_field(
            name="!",
            value=f"{member} Was muted.\nReason:{reason}",
            inline=False
        )
        role = await self._get_mute_role(ctx.guild)

        await member.add_roles(role)
        await ctx.send(embed=embed)

    @commands.command(help="Unmute a member.",aliases=['demute', 'um'])
    @commands.has_permissions(kick_members=True)
    async def unmute(self,
                     ctx,
                     member: discord.Member, *,
                     reason="Reason not provided."):
        embed = discord.Embed(
            colour=discord.Colour.blue(),
            title="__Unmute__"
        )
        embed.add_field(
            name="!",
            value=f"{member} Was muted.\nReason:{reason}",
            inline=False
        )
        role = await self._get_mute_role(ctx.guild)

        await member.remove_roles(role)
        await ctx.send(embed=embed)

    @commands.command(help="Warn is a member",aliases=['w'])
    @commands.has_permissions(kick_members=True)
    async def warn(self,
                   ctx,
                   member: discord.Member, *,
                   reason="Reason not provided."):
        channel = discord.utils.get(ctx.guild.text_channels, name='warn-logs')

        if channel is None:
            channel = await ctx.guild.create_text_channel('warn-logs')
        embed = discord.Embed(color=discord.Color.blue())
        embed.set_author(name='Warning')
        embed.add_field(
            name='!',
            value=f'{member} has been warned because: {reason}',
            inline=False
        )

        await member.send(embed=embed)
        await channel.send(embed=embed)

    @commands.command(help="Start a giveaway.",aliases=['g'])
    @commands.has_permissions(administrator=True)
    @commands.is_owner()
    async def giveaway(self, ctx, seconds: int, *, prize):
        task = self.bot.loop.create_task(self._do_giveaway(ctx, seconds, prize))
        self._giveaways.append(task)


def setup(bot):
    bot.add_cog(Moderation(bot))
