import discord
from discord.ext import commands
import dislash
from dislash import slash_commands


class InfoPaginator(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    async def paginator(self):
        ...

    @commands.command(name="info")
    async def info(self, ctx: commands.Context) -> None:
        await ctx.message.delete()


def setup(bot: commands.Bot) -> None:
    bot.add_cog(InfoPaginator(bot))
