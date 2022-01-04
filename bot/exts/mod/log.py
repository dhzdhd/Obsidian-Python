import datetime

import discord
from discord.ext import commands

from bot.utils.database import AuditDatabase
from bot.utils.embed import ErrorEmbed, SuccessEmbed


class AuditLog(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.group(name="audit", aliases=("log",), invoke_without_command=True)
    @commands.has_permissions(manage_guild=True)
    async def audit_log_group(self, ctx: commands.Context) -> None:
        await ctx.message.delete()
        await ctx.send_help()

    @audit_log_group.command(name="new", aliases=("n", "add", "a"))
    @commands.has_permissions(manage_guild=True)
    async def create_audit_log(self, ctx: commands.Context, channel: discord.TextChannel = None) -> None:
        await ctx.message.delete()

        check = await AuditDatabase.get_id(self.bot, ctx.guild)
        if check is not None:
            embed = ErrorEmbed(
                description="This server already has a log channel!",
                author=ctx.author
            )
            await ctx.send(embed=embed, delete_after=20)
            return

        permissions = {
            ctx.guild.default_role: discord.PermissionOverwrite(read_messages=False)
        }

        if channel is None:
            await ctx.guild.create_category(name="AUDIT LOG")
            channel = await ctx.guild.create_text_channel(name="log", permissions=permissions)

        await AuditDatabase.store_id(self.bot, guild=ctx.guild, channel=channel)

        embed = SuccessEmbed(
            description=f"Log channel successfully made!\nChannel name: **{channel.name}**",
            author=ctx.author
        )
        await ctx.send(embed=embed, delete_after=60)

    @audit_log_group.command(name="delete", aliases=("del", "d", "remove", "rem", "r"))
    @commands.has_permissions(manage_guild=True)
    async def delete_log(self, ctx: commands.Context) -> None:
        await ctx.message.delete()

        channel = await AuditDatabase.get_id(self.bot, ctx.guild)
        if channel is None:
            embed = ErrorEmbed(
                description="This server does not have a log channel!",
                author=ctx.author
            )
            await ctx.send(embed=embed, delete_after=20)
            return

        await channel.delete()
        await AuditDatabase.delete_id(self.bot, ctx.guild)

        embed = SuccessEmbed(
            "Log successfully deleted!",
            ctx.author
        )
        await ctx.send(embed=embed, delete_after=60)

    @audit_log_group.command(name="update", aliases=("u",))
    @commands.has_permissions(manage_guild=True)
    async def update_log(self, ctx: commands.Context, channel: discord.TextChannel) -> None:
        await ctx.message.delete()

        channel = await AuditDatabase.get_id(self.bot, ctx.guild)
        if channel is None:
            embed = ErrorEmbed(
                description="This server does not have a log channel!",
                author=ctx.author
            )
            await ctx.send(embed=embed, delete_after=20)
            return

        await AuditDatabase.update_id(self.bot, ctx.guild, channel)

        embed = SuccessEmbed(
            description=f"Successfully updated log channel!\nNew log channel: **{channel.name}**",
            author=ctx.author
        )
        await ctx.send(embed=embed, delete_after=60)


def setup(bot: commands.Bot) -> None:
    bot.add_cog(AuditLog(bot))
