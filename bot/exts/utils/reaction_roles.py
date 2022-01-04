import datetime
from typing import Union

import discord
from discord.ext import commands


class ReactionRoles(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.group(name="reactionrole", aliases=("rr",), invoke_without_command=True)
    @commands.has_permissions(manage_guild=True)
    async def reaction_role_group(self, ctx: commands.Context) -> None:
        await ctx.message.delete()
        await ctx.send_help(ctx.command)

    @reaction_role_group.command(name="add", aliases=("a",))
    @commands.has_permissions(manage_guild=True)
    async def add_role(
        self,
        ctx: commands.Context,
        role: discord.Role,
        emoji: Union[discord.Emoji, discord.PartialEmoji],
        *,
        info: str
    ) -> None:
        await ctx.message.delete()


def setup(bot: commands.Bot) -> None:
    bot.add_cog(ReactionRoles(bot))
