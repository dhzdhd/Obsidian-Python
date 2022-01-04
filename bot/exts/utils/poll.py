""" Poll Cog for Obsidian bot """

# Imports
import discord
from discord.ext import commands
import datetime
import re
import json
import asyncio
import logging


class PollCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.count_dict = {}
        self.total_count = {}
        self.poll_check_dict = {}

        self.poll_emoji_list = [
            "1️⃣",
            "2️⃣",
            "3️⃣",
            "4️⃣",
            "5️⃣",
            "6️⃣",
            "7️⃣",
            "8️⃣",
            "9️⃣",
        ]

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):

        if (
            payload.guild_id in self.poll_check_dict.keys()
            and payload.message_id in self.poll_check_dict.values()
            and payload.user_id != self.bot.user.id
        ):
            if payload.emoji.name == self.poll_emoji_list[0]:
                self.total_count[self.poll_msgid] += 1
                self.count_dict[self.choices[0]][1] += 1
                self.poll_embed.remove_field(0)
                self.poll_embed.insert_field_at(
                    0,
                    name=f"{self.poll_emoji_list[0]} : {self.choices[0]}",
                    value=f"{self.count_dict[self.choices[0]][1]/self.total_count[self.poll_msgid]*100}% ({self.count_dict[self.choices[0]][1]})",
                    inline=False,
                )
                self.edit_msg = await payload.member.fetch_message(
                    self.poll_check_dict[payload.guild_id]
                )  # wrong !! F
                await self.edit_msg.edit(embed=self.poll_embed)

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        ...

    @commands.has_permissions(manage_guild=True)
    @commands.command(aliases=["p"])
    async def poll(self, ctx, *, raw_str):
        if "[" in raw_str:
            self.topic = re.findall("\[(.*?)\]", raw_str)[0]
            self.choices = raw_str.split(",")
            self.choices[0] = self.choices[0].partition("]")[2]
        else:
            self.topic = "No topic selected"
            self.choices = raw_str.split(",")

        self.poll_embed = discord.Embed(
            colour=discord.Colour.dark_teal(), timestamp=datetime.datetime.utcnow()
        )
        self.poll_embed.set_author(name=f"Poll : {self.topic.capitalize()}")
        self.poll_embed.set_footer(
            text=f"Requested by : {ctx.author.name}", icon_url=ctx.author.avatar_url
        )
        for _ in range(len(self.choices)):
            self.poll_embed.add_field(
                name=f"{self.poll_emoji_list[_]} : {self.choices[_]}",
                value=f"0% (0)",
                inline=False,
            )

        self.poll_msg = await ctx.send(embed=self.poll_embed)
        self.poll_msgid = self.poll_msg.id

        for _ in range(len(self.choices)):
            await self.poll_msg.add_reaction(self.poll_emoji_list[_])

        self.poll_check_dict[ctx.guild.id] = self.poll_msgid
        for _ in self.choices:
            self.count_dict[_] = [self.poll_msgid, 0]
        self.total_count[self.poll_msgid] = 0


def setup(bot):
    """ Setup function for poll Cog """
    bot.add_cog(PollCommand(bot))
