import datetime
from typing import Union

from discord import Member, TextChannel
from discord.ext import commands, tasks


class BirthdayCommands(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot
        self.send_bday_msgs.start()
        self.time_to_send = datetime.timedelta(hours=9)  # Send the message at about 9 AM IST

    @tasks.loop(hours=24)
    async def send_bday_msgs(self) -> None:
        """Loop to send birthday message according to the matching date with the database data"""
        async with self.bot.asyncpg_pool.acquire() as pool:
            await pool.execute()

    @send_bday_msgs.before_loop
    async def ready(self) -> None:
        """Wait for the bot to get ready."""
        await self.bot.wait_until_ready()

    @commands.group(
        name="birthday",
        aliases=("bday",),
        invoke_without_command=True
    )
    async def birthday_group(self, ctx) -> None:
        """Birthday group of commands."""
        await ctx.send_help(ctx.command)

    @birthday_group.command(name="create")
    async def create_bday(
        self,
        ctx: commands.Context,
        text_channel: TextChannel,
        member: Union[Member, int],
        date: int,  # MM-DD
    ) -> None:
        """Register a user birthday with the database."""
        await ctx.message.delete()

        async with self.bot.asyncpg_pool() as pool:
            await pool.execute(
                "INSERT INTO bdaydb VALUES($1, $2, $3)",
                text_channel.id,
                member.id,
                date
            )

    @birthday_group.command(name="show")
    @commands.is_owner()
    async def show_bdays(
            self,
            ctx: commands.Context,
            guild: Union[int, str]
    ) -> None:
        """
        Show all the birthdays of all users of a certain guild.

        Available only for the owner of the bot.
        """
        await ctx.message.delete()
        ...


def setup(bot):
    bot.add_cog(BirthdayCommands(bot))
