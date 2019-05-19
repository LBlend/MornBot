from discord.ext import commands

import traceback
import sys

from .utils import Defaults


class Errors(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if hasattr(ctx.command, 'on_error'):
            return

        ignored = commands.CommandNotFound
        send_help = (commands.MissingRequiredArgument,
                     commands.TooManyArguments,
                     commands.BadArgument)

        error = getattr(error, 'original', error)

        if isinstance(error, ignored):
            return

        elif isinstance(error, send_help):
            return await ctx.send_help(ctx.command)

        elif isinstance(error, commands.BotMissingPermissions):
            permissions = ', '.join(error.missing_perms)
            return await ctx.send(
                f'Jeg mangler følgende tillatelser:\n\n```{permissions}```')

        elif isinstance(error, commands.NotOwner):
            return await Defaults.error_fatal_send(
                ctx, text='Du er ikke båtteier', mention=False)

        elif isinstance(error, commands.MissingPermissions):
            permissions = ', '.join(error.missing_perms)
            return await Defaults.error_warning_send(
                ctx,
                text='Du mangler følgende ' +
                     f'tillatelser:\n\n```{permissions}```',
                mention=False)

        elif isinstance(error, commands.CommandOnCooldown):
            return await Defaults.error_warning_send(
                ctx,
                text='Kommandoen har nettopp blitt brukt. Prøv igjen om ' +
                     f'`{error.retry_after:.1f}` sekunder.')

        elif isinstance(error, commands.NSFWChannelRequired):
            return await Defaults.error_fatal_send(
                ctx, text='Du må være i en NSFW-Kanal', mention=False)

        elif isinstance(error, commands.NoPrivateMessage):
            try:
                return await Defaults.error_fatal_send(
                    ctx,
                    text=f'`{ctx.command}` kan ikke brukes i DMs',
                    mention=False)
            except:
                pass

        print('Ignoring exception in command {}:'.format(ctx.command),
              file=sys.stderr)
        traceback.print_exception(type(error), error, error.__traceback__,
                                  file=sys.stderr)


def setup(bot):
    bot.add_cog(Errors(bot))
