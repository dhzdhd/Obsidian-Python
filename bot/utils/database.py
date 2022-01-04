import discord
from discord.ext import commands
from typing import Union


class AuditDatabase:
    @staticmethod
    async def get_id(bot: commands.Bot, guild: discord.Guild) -> Union[discord.TextChannel, int, None]:
        async with bot.asyncpg_pool.acquire() as pool:
            try:
                cid = await pool.fetchrow(
                    "SELECT channel FROM log WHERE guild=$1", guild.id
                )

                if cid is None:
                    return None

                cid = cid[0]
                return discord.utils.get(guild.channels, id=id)
            except:
                return 1

    @staticmethod
    async def store_id(bot: commands.Bot, guild: discord.Guild, channel: discord.TextChannel) -> None:
        async with bot.asyncpg_pool.acquire() as pool:
            await pool.execute(
                "INSERT INTO log VALUES($1, $2)",
                guild.id,
                channel.id
            )

    @staticmethod
    async def delete_id(bot: commands.Bot, guild: discord.Guild) -> None:
        async with bot.asyncpg_pool.acquire() as pool:
            await pool.execute(
                "DELETE FROM log WHERE guild=$1",
                guild.id
            )

    @staticmethod
    async def update_id(bot: commands.Bot, guild: discord.Guild, channel: discord.TextChannel) -> None:
        async with bot.asyncpg_pool.acquire() as pool:
            await pool.execute(
                "UPDATE log SET channel=$1 WHERE guild=$2",
                channel.id,
                guild.id
            )
