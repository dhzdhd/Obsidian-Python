""" Levels Cog for Obsidian bot """

# Imports
import discord
from discord.ext import commands
import datetime
from urllib import request
import json
from PIL import Image, ImageFont
from io import BytesIO as bIO


class LevelSystem(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.url = "https://4.bp.blogspot.com/-lt2Qa0hjES8/WQ7FTMMiZZI/AAAAAAAAAdI/2oiXbq2rVbguF85_y-f-K6BPRVbPOt3XQCLcB/s640/Amazing%2BLandscape%2BWE.jpg"

        response = request.urlopen(self.url)
        self.bg_image = Image.open(response)
        self.bg_image = self.bg_image.convert("RGBA")

    def make_level_image(self, author=None):
        image = self.bg_image.copy()

        buffer = bIO()
        image.save(buffer, format="PNG")
        buffer.seek(0)
        return buffer

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author != self.bot.user:
            pass

    @commands.command(aliases=["rank", "lvl"])
    async def level(self, ctx):
        await ctx.message.delete()

        final_img = self.make_level_image()
        await ctx.send(file=discord.File(final_img, "hmm.png"))


def setup(bot):
    """ Setup function for levels Cog """
    bot.add_cog(LevelSystem(bot))
