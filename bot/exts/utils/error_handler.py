from discord.ext import commands

from utils.embed_helper import ErrorEmbed


class ErrorHandler(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            error_embed = ErrorEmbed(
                description=f"Command on cooldown\n\nRetry after **{round(error.retry_after)}** seconds",
                author=ctx.author
            )
            await ctx.send(embed=error_embed, delete_after=15)
            return
    
        if isinstance(error, commands.MissingRequiredArgument):
            error_embed = ErrorEmbed(
                description="Command missing required arguments\n\nFor more info refer to `>help <command>`",
                author=ctx.author
            )
            await ctx.send(embed=error_embed, delete_after=15)
            return
    
        if isinstance(error, commands.TooManyArguments):
            error_embed = ErrorEmbed(
                description="Command received too many arguments\n\nFor more info refer to `>help <command>`",
                author=ctx.author
            )
            await ctx.send(embed=error_embed, delete_after=15)
            return
    
        if isinstance(error, commands.CommandError):
            error_embed = ErrorEmbed(
                description="Command has an error\n\n For more info refer to `>help <command>`",
                author=ctx.author
            )
            await ctx.send(embed=error_embed, delete_after=15)


def setup(bot):
    """ErrorEvents Cog setup."""
    bot.add_cog(ErrorHandler(bot))
