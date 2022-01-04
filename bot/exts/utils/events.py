import discord
from discord.ext import commands, tasks

from utils.embed_helper import Audit


class BotEvents(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @tasks.loop()
    async def change_presence(self) -> None:
        ...

    @commands.Cog.listener()
    async def on_ready(self):
        """ Code to be executed on bot login and connect """
        self.game = discord.Game(f">info | {len(self.bot.guilds)} servers")
        await self.bot.change_presence(activity=self.game)

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        """Discord on_message event handler."""
        if message.author != self.bot.user:
            if self.bot.user in message.mentions:
                await message.channel.send("Hello there! :smile:")

            if (
                "despacito" in message.content.lower()
                and "alexa" in message.content.lower()
            ) or "this is so sad" in message.content.lower():
                await message.channel.send(
                    "Alexa playing despacito:\nhttps://www.youtube.com/watch?v=W3GrSMYbkBE"
                )

            if message.content == ".":
                await message.channel.send("point")

            if message.content == ",":
                await message.channel.send("ok")

    @commands.Cog.listener()
    async def on_message_delete(self, message: discord.Message) -> None:
        if message.author != self.bot.user:
            channel = await Audit._get_id(self.bot, message.guild)
            if isinstance(channel, discord.TextChannel):
                await channel.send(
                    embed=Audit(
                        title="Message deleted",
                        description=f"{message.content}",
                        author=message.author,
                        _type="msg_delete"
                    )
                )

    @commands.Cog.listener()
    async def on_message_edit(self, before: discord.Message, after: discord.Message) -> None:
        if before.author != self.bot.user and not before.content.startswith("https://"):
            channel = await Audit._get_id(self.bot, before.guild)
            if isinstance(channel, discord.TextChannel):
                await channel.send(
                    embed=Audit(
                        title="Message edited",
                        description=f"Before : ```{before.content}```\nAfter : ```{after.content}```",
                        author=before.author,
                        _type="msg_edit"
                    )
                )


def setup(bot):
    """setup function for events Cog."""
    bot.add_cog(BotEvents(bot))
