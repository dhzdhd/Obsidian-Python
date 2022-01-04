import asyncio
import datetime

import discord
from discord.ext import commands
from dislash import Option, Type
from dislash import slash_commands
from dislash.interactions import SlashInteraction

from bot.utils.constants import Colours
from bot.utils.embed import ErrorEmbed


class MuteUnmute(commands.Cog):
    """
    MuteUnmute cog, containing commands related to the mutes and unmutes in text and voice channels.

    Commands
        ├ mute          Mute a given user given the id/name/mention of the user for a given amount of time
                        specified in the command which takes a default of 5 minutes, along with a reason
        └ unmute        ...
    """

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @staticmethod
    async def _manage_role(ctx: SlashInteraction, user: discord.Member) -> discord.Role:
        role: discord.Role = discord.utils.get(ctx.guild.roles, name="Muted")

        if not role:
            role = await ctx.guild.create_role(
                name="Muted",
                permissions=discord.Permissions(send_messages=False),
                colour=discord.Colour.red(),
                reason="A mute role"
            )

        return role

    @slash_commands.command(
        name="mute",
        description="Mute a member for a given amount of time",
        options=[
            Option("user", "The member to be muted", Type.USER, required=True),
            Option("time", "Mute time in minutes", Type.INTEGER, required=False),
            Option("reason", "Reason for the mute", Type.STRING, required=False)
        ]
    )
    @slash_commands.has_permissions(manage_guild=True)
    async def mute(self, ctx: SlashInteraction) -> None:
        """Mutes a user for a specified amount of time (defaulted to 5 minutes)"""
        user = ctx.get("user")
        time = ctx.get("time")
        reason = ctx.get("reason")

        role = await self._manage_role(ctx, user)

        mute_embed = discord.Embed(
            title=f"Muted user: **{user.display_name}**",
            colour=Colours.AUDIT_COLORS["mod"],
            description=f"Time: **{time} minutes**\n\nReason: \n*{reason}*",
            timestamp=datetime.datetime.utcnow(),
        ).set_footer(text=f"Invoked by {ctx.author.name}", icon_url=ctx.author.avatar_url)
        unmute_embed = discord.Embed(
            title=f"Unmuted user: **{user.display_name}**",
            colour=Colours.AUDIT_COLORS["mod"],
            description=f"The mute duration of {time} minutes has ended.",
            timestamp=datetime.datetime.utcnow(),
        ).set_footer(text=f"Invoked by {ctx.author.name}", icon_url=ctx.author.avatar_url)
        perms_embed = discord.Embed(
            title=f"Unmuted user: **{user.display_name}**",
            colour=Colours.AUDIT_COLORS["mod"],
            description=f"The mute duration of {time} minutes has ended.",
            timestamp=datetime.datetime.utcnow(),
        ).set_footer(text=f"Invoked by {ctx.author.name}", icon_url=ctx.author.avatar_url)

        async with self.bot.asyncpg_pool.acquire() as pool:
            result = await pool.fetchrow("SELECT mutes FROM mod WHERE id=$1 AND guild=$2", user.id, user.guild.id)

            if not result:
                await pool.execute(
                    "INSERT INTO mod(id, name, guild, mutes) VALUES($1, $2, $3, $4)",
                    user.id,
                    user.display_name,
                    user.guild.id,
                    1
                )
            else:
                await pool.execute(
                    "UPDATE mod SET mutes=$1 WHERE id=$2 AND guild=$3",
                    int(result["mutes"]) + 1,
                    user.id,
                    user.guild.id
                )

        await ctx.reply(embed=mute_embed, delete_after=60)

        await user.add_roles(role)
        await asyncio.sleep(time*60)
        await user.remove_roles(role)

        await ctx.reply(embed=unmute_embed, delete_after=60)

    @slash_commands.command(
        name="unmute",
        description="Unmute a muted member",
        options=[
            Option("user", "Member to be unmuted", Type.USER, required=True)
        ]
    )
    @slash_commands.has_permissions(manage_guild=True)
    async def unmute(self, ctx: SlashInteraction) -> None:
        user = ctx.get("user")

        unmute_embed = discord.Embed(
            title=f"Unmuted user: **{user.display_name}**",
            colour=Colours.AUDIT_COLORS["mod"],
            description=f"The mute has been lifted.",
            timestamp=datetime.datetime.utcnow(),
        ).set_footer(text=f"Invoked by {ctx.author.name}", icon_url=ctx.author.avatar_url)
        error_embed = ErrorEmbed(
            "User is not muted!",
            ctx.author
        )

        muted_role = discord.utils.get(ctx.guild.roles, name="Muted")

        if muted_role in user.roles:
            await user.remove_roles(muted_role)
            await ctx.reply(embed=unmute_embed, delete_after=15)
        else:
            await ctx.reply(embed=error_embed, delete_after=15)


def setup(bot: commands.Bot) -> None:
    """Load the MuteUnmute cog."""
    bot.add_cog(MuteUnmute(bot))
