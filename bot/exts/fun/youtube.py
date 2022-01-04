""" Youtube Cog for Obsidian bot """

# Imports
import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
import datetime
import aiohttp

# from ..main import Logger


class YoutubeCommand(commands.Cog):
    """ YoutubeCommand Cog """

    def __init__(self, bot):
        self.bot = bot

        load_dotenv()
        self.YT_KEY = os.getenv("YT_KEY")

        self.url = "https://www.googleapis.com/youtube/v3/search/"
        self.params = dict(
            key=self.YT_KEY,
            part="snippet",
            maxResults=10,
            videoEmbeddable="true",
            type="video",
        )
        self.location = "(37.0902,95.7129)"

    @commands.cooldown(rate=1, per=20, type=commands.BucketType.user)
    @commands.command(name="youtube", aliases=["yt"])
    async def youtube(self, ctx, *, search):
        """ Gets a yt vid url which when sent to the channel opens as an embed based on a query """
        await ctx.message.delete()
        self.params["q"] = search

        try:
            async with ctx.typing():
                async with self.bot.http_session.get(url=self.url, params=self.params) as response:
                    json = await response.json()
                vid = json["items"][0]["id"]["videoId"]

                yt_embed = discord.Embed(
                    title=f"Searched for video | Query : {search}",
                    colour=discord.Colour.red(),
                    timestamp=datetime.datetime.utcnow(),
                )
                yt_embed.set_footer(
                    text=f"Requested by {ctx.author.name}",
                    icon_url=ctx.author.avatar_url,
                )
                await ctx.send(embed=yt_embed)
                await ctx.send(f"https://www.youtube.com/watch?v={vid}")

        except aiohttp.ClientResponseError as e:
            if e.status == 403:
                await ctx.send(
                    "YT API Quota finished. Sorry for the inconvenience",
                    delete_after=60,
                )

        except KeyError:
            await ctx.send(
                "The requested video was not found. Try with a different query",
                delete_after=10,
            )


def setup(bot):
    """ Setup function for youtube Cog """
    bot.add_cog(YoutubeCommand(bot))
