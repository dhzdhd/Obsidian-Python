import datetime
import os

import aiohttp
import asyncio
import discord
from discord.ext import commands
from dotenv import load_dotenv
from typing import Dict

from obsidian.utils.embed_helper import ErrorEmbed


class CodeExecutor(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.lang = None

        self.url = "https://emkc.org/api/v2/piston/execute"
        asyncio.ensure_future(self._setup_lang())

    async def _setup_lang(self) -> None:
        _dict = {}

        async with aiohttp.ClientSession() as session:
            async with session.get(url="https://emkc.org/api/v2/piston/runtimes") as resp:
                json = await resp.json()
                for element in json:
                    _dict[element['language']] = element['version']

        self.lang_dict = _dict
        print(self.lang_dict)

    @commands.group(name="eval", invoke_without_context=True)
    async def eval_command(self):
        ...

    @eval_command.command(name="code", aliases=("exec", "eval"))
    @commands.cooldown(rate=1, per=5, type=commands.BucketType.user)
    async def code_execution(self, ctx, *, code: str):
        await ctx.message.delete()

        code = code.strip('```')
        self.lang = code.partition('\n')[0]
        code = code.lstrip(self.lang)

        _data = {
            "language": self.lang,
            "version": self.lang_dict[self.lang],
            "files": [
                {
                    "content": code
                }
            ]
        }

        async with aiohttp.ClientSession() as session:
            async with session.post(url=self.url, data=_data) as resp:
                json = await resp.json()
                print(json)


def setup(bot):
    """ CodeExecutor Cog setup """
    bot.add_cog(CodeExecutor(bot))
