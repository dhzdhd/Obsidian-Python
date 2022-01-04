import datetime

import discord
from discord.ext import commands


class Utilities(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.command(name="say")
    @commands.has_permissions(manage_guild=True)
    async def say_message(
        self,
        ctx: commands.Context,
        channel: discord.TextChannel,
        *,
        message: str
    ) -> None:
        await ctx.message.delete()
        await channel.send(message)

    @commands.command(name="dm")
    @commands.has_permissions(manage_guild=True)
    async def send_dm(
        self,
        ctx: commands.Context,
        user: discord.Member,
        embed: bool = False,
        *,
        message: str
    ) -> None:
        await ctx.message.delete()

        parsed_dict = {
            "title": message.partition(""),
            "desc": ""
        }
        embed = discord.Embed(
            title=parsed_dict["title"],
            description=parsed_dict["desc"],
            colour=discord.Colour.dark_green(),
            timestamp=datetime.datetime.utcnow()
        ).set_footer(text=f"Invoked by {ctx.author.name}", icon_url=ctx.author.avatar_url)

        if not embed:
            await user.send(message)
            return
        await user.send(embed=embed)


def setup(bot: commands.Bot) -> None:
    bot.add_cog(Utilities(bot))
