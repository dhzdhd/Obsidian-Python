from dislash.slash_commands import SlashClient

import bot


if __name__ == "__main__":
    bot = bot.Bot()
    slash = SlashClient(
        client=bot,
        show_warnings=True
    )

    @slash.event
    async def on_ready():
        ...
        # await slash_client.delete_global_commands()
        # await slash_client.delete_guild_commands(771778089779855391)

    try:
        bot.run()
    except KeyboardInterrupt:
        bot.close()
