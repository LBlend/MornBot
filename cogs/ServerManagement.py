import discord
from discord.ext import commands

from cogs.utils import Defaults


class ServerManagement(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.bot_has_permissions(kick_members=True)
    @commands.has_permissions(kick_members=True)
    @commands.guild_only()
    @commands.cooldown(1, 2, commands.BucketType.guild)
    @commands.command(aliases=['spark'])
    async def kick(
            self, ctx, bruker: discord.Member, *, begrunnelse: str=None):
        """Kaster ut en bruker fra serveren"""

        await bruker.kick(reason=begrunnelse)
        await ctx.send(f'{bruker.mention} ' +
                       f'`{bruker.name}#{bruker.discriminator}` ' +
                       'ble kastet ut av serveren')

    @commands.bot_has_permissions(ban_members=True)
    @commands.has_permissions(ban_members=True)
    @commands.guild_only()
    @commands.cooldown(1, 2, commands.BucketType.guild)
    @commands.command()
    async def ban(self, ctx, bruker: discord.Member, *, begrunnelse: str=None):
        """Utesteng en bruker fra serveren"""

        await bruker.ban(reason=begrunnelse)
        await ctx.send(f'{bruker.mention} ' +
                       f'`{bruker.name}#{bruker.discriminator}` ' +
                       'ble utestengt fra serveren')

    @commands.bot_has_permissions(manage_messages=True)
    @commands.has_permissions(manage_messages=True)
    @commands.cooldown(1, 30, commands.BucketType.guild)
    @commands.command(aliases=['purge', 'delete', 'slett'])
    async def prune(self, ctx, antall: int):
        """Sletter de siste antall meldingene du spesifiser"""

        if antall > 100:
            return await Defaults.error_warning_send(
                ctx,
                text='Du kan ikke slette mer enn 100 meldinger om gangen',
                mention=False)

        await ctx.channel.purge(limit=antall+1)
        await ctx.send(content=f'Slettet `{antall}` meldinger!',
                       delete_after=3.0)


def setup(bot):
    bot.add_cog(ServerManagement(bot))
