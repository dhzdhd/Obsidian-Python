import datetime

import discord
from discord.ext import commands

from bot.utils.embed import SuccessEmbed


# Add embed support
class Bookmark(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self._dict = {}

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload) -> None:
        if payload.user_id != self.bot.user.id:
            if payload.emoji == discord.PartialEmoji(name="📩"):
                await payload.member.send(embed=self._dict[int(payload.message_id)])

            elif payload.emoji == discord.PartialEmoji(name="❌"):
                channel = await self.bot.fetch_channel(payload.channel_id)
                message = await channel.fetch_message(payload.message_id)
                await message.delete()

    @commands.command(name="bookmark", aliases=("bm",))
    async def bookmark(self, ctx: commands.Context, message_id: int = None) -> None:
        await ctx.message.delete()

        if message_id is None:
            if ctx.message.reference is None:
                return
            message = await ctx.fetch_message(ctx.message.reference.message_id)
        else:
            message = await ctx.fetch_message(message_id)

        dm_embed = discord.Embed(
            title="Bookmarked message",
            description=f"Author: **{message.author.name}**\nContents:\n{message.content}",
            colour=discord.Colour.blue(),
            timestamp=datetime.datetime.utcnow()
        ).set_footer(text=f"Invoked by {ctx.author.name}", icon_url=ctx.author.avatar_url)
        reaction_embed = SuccessEmbed(
            description=f"**Message bookmarked!**\nLink to message: \n{message.jump_url}",
            author=ctx.author
        )

        msg = await ctx.send(embed=reaction_embed, delete_after=3600)
        await msg.add_reaction("📩")
        await msg.add_reaction("❌")
        self._dict.update({int(msg.id): dm_embed})

        await ctx.author.send(embed=dm_embed)


def setup(bot: commands.Bot) -> None:
    bot.add_cog(Bookmark(bot))
