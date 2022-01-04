import asyncpraw
from discord.ext import commands

from bot.utils.constants import Tokens


class Reddit:
    def __init__(self) -> None:
        self.reddit = asyncpraw.Reddit(
            client_id=Tokens.REDDIT_ID,
            client_secret=Tokens.REDDIT_SECRET,
            user_agent=Tokens.REDDIT_AGENT,
            username=Tokens.REDDIT_USERNAME,
            password=Tokens.REDDIT_PASSWORD
        )
        self.reddit.read_only = True


class RedditCommands(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.reddit = asyncpraw.Reddit(
            client_id=Tokens.REDDIT_ID,
            client_secret=Tokens.REDDIT_SECRET,
            user_agent=Tokens.REDDIT_AGENT,
            username=Tokens.REDDIT_USERNAME,
            # password=Tokens.REDDIT_PASSWORD
        )
        # self.reddit.read_only = True
        # self.reddit: asyncpraw.Reddit = Reddit()

    @commands.group(name="reddit", aliases=("re",), invoke_without_command=True)
    async def reddit_group(self, ctx: commands.Context) -> None:
        await ctx.message.delete()
        await ctx.send_help(ctx.command)

    @reddit_group.command(name="meme", aliases=("m",))
    async def reddit_meme(self, ctx: commands.Context) -> None:
        await ctx.message.delete()

        await ctx.send(await self.reddit.user.me())


def setup(bot: commands.Bot) -> None:
    bot.add_cog(RedditCommands(bot))
