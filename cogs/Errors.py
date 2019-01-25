import discord
from discord.ext.commands import errors
import traceback

class Errors:
    def __init__(self, bot):
        self.bot = bot

    async def on_command_error(self, ctx, err):
        if (isinstance(err, errors.MissingRequiredArgument) or isinstance(err, errors.BadArgument)):
            formatter = ctx.bot.formatter
            if ctx.invoked_subcommand is None:
                _help = await formatter.format_help_for(ctx, ctx.command)
            else:
                _help = await formatter.format_help_for(ctx, ctx.invoked_subcommand)

            for message in _help:
                await ctx.send(message)

        if isinstance(err, errors.CommandInvokeError):
            pass

        elif isinstance(err, errors.NoPrivateMessage):
            await ctx.send("Denne kommandoen er ikke tilgjengelig i DMs")

        elif isinstance(err, errors.CheckFailure):
            pass

        elif isinstance(err, errors.CommandNotFound):
            pass

        elif isinstance(err, errors.NotOwner):
            await ctx.send("Du er ikke dev av båtten")

        elif isinstance(err, errors.MissingPermissions):
            await ctx.send("Du mangler tillatelse til å gjøre dette")

        elif isinstance(err, errors.BotMissingPermissions):
            await ctx.send("Jeg mangler tillatelse til å gjøre dette")

        elif isinstance(err, errors.CommandOnCooldown):
            await ctx.send(f"{ctx.message.author.mention} Kommandoen har nettopp blitt brukt. Prøv igjen om `{err.retry_after:.1f}` sekunder.")

        else:
            tb = err.__traceback__             
            traceback.print_tb(tb)             
            print(err)

def setup(bot):
    bot.add_cog(Errors(bot))