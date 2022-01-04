import os
from datetime import datetime, timedelta
from typing import Union

import discord
from discord import TextChannel
from discord.ext.commands import Cog, command, has_permissions, is_owner, Context
from discord.ext.tasks import loop
from dotenv import load_dotenv

from constants import Emojis


class YoutubeUpdates(Cog):
    def __init__(self, bot):
        self.bot = bot

        load_dotenv()
        self.YT_KEY = os.getenv("YT_KEY")
        self.time = datetime.utcnow()
        self.thirty_min = timedelta(minutes=30)
        self.final_time = str(self.time - self.thirty_min)

        self.url = "https://www.googleapis.com/youtube/v3/search/"
        self.params = dict(
            key=self.YT_KEY,
            part="snippet",
            maxResults=10,
            videoEmbeddable="true",
            publishedAfter=f"{self.final_time[:10]}T{self.final_time[11:19]}Z",
            type="video",
        )
        self.location = "(37.0902,95.7129)"

        self.get_youtube_updates.start()

    @loop(minutes=10)
    async def get_youtube_updates(self):

        async with self.bot.asyncpg_pool.acquire() as pool:
            await pool.execute(
                "CREATE TABLE IF NOT EXISTS botytid(channelid TEXT PRIMARY KEY,guild BIGINT NOT NULL,tc BIGINT NOT NULL)"
            )
        records = await self.bot.asyncpg_pool.fetch("SELECT * FROM botytid")
        for _ in tuple(records):
            temp_dict = dict(_)
            channel_id = temp_dict["channelid"]

            self.params["channelId"] = channel_id

            response = await self.bot.http_session.get(url=self.url, params=self.params)
            guild = self.bot.get_guild(temp_dict["guild"])
            tc = guild.get_channel(temp_dict["tc"])
            json = response[2]

            try:
                vid_id = json["items"][0]["id"]["videoId"]
                await tc.send(f"https://www.youtube.com/watch?v={vid_id}")
            except (IndexError, Exception):
                pass

    @get_youtube_updates.before_loop
    async def before_update(self):
        await self.bot.wait_until_ready()

    @has_permissions(manage_guild=True)
    @command(
        name="sub"
    )
    async def sub(
        self, ctx: Context, cid: str, tcid: Union[int, TextChannel], guildid: int = None
    ) -> None:
        if isinstance(tcid, TextChannel):
            tcid = tcid.id

        if guildid is None:
            tchannel = discord.utils.get(ctx.guild.channels, id=tcid)
            await self.bot.asyncpg_pool.execute(
                "INSERT INTO botytid VALUES($1,$2,$3)", cid, ctx.guild.id, tcid
            )
        else:
            guild = self.bot.get_guild(guildid)
            tchannel = guild.get_channel(tcid)
            await self.bot.asyncpg_pool.execute(
                "INSERT INTO botytid VALUES($1,$2,$3)", cid, guildid, tcid
            )

        subbed_embed = discord.Embed(
            title=f"{Emojis.TICK} Success",
            description="Successfully saved channel id into database\n"
            f"Updates will now be sent to **{tchannel.name}**",
            colour=discord.Colour.green(),
            timestamp=datetime.utcnow(),
        )
        subbed_embed.set_footer(
            text=f"Requested by {ctx.author.name}", icon_url=ctx.author.avatar_url
        )
        await ctx.send(embed=subbed_embed)

    @has_permissions(manage_guild=True)
    @command(
        name="unsub",
        brief="unsub afgiefgjei",
        description="""grorj
                    """,
        aliases=["unsob"],
    )
    async def unsub(self, ctx, cid: str):
        try:
            await self.bot.asyncpg_pool.execute(
                "DELETE FROM botytid WHERE channelid=$1", cid
            )
        except:
            await ctx.send("Invalid channel ID", delete_after=10)
            return

        unsubbed_embed = discord.Embed(
            title=f"{Emojis.TICK} Success",
            description="Successfully deleted information from database\n",
            colour=discord.Colour.green(),
            timestamp=datetime.utcnow(),
        )
        unsubbed_embed.set_footer(
            text=f"Requested by {ctx.author.name}", icon_url=ctx.author.avatar_url
        )
        await ctx.send(embed=unsubbed_embed)

    @is_owner()
    @command()
    async def getytdb(self, ctx):
        records = await self.bot.asyncpg_pool.fetch("SELECT channelid FROM botytid")
        await ctx.send(records)


def setup(bot):
    bot.add_cog(YoutubeUpdates(bot))
