from discord.ext import commands
import discord

import pymongo

from cogs.utils import Defaults


class ServerManagement(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.database_col_cog_check = pymongo.MongoClient(self.bot.database)['discord']['cog_check']

    @commands.bot_has_permissions(kick_members=True)
    @commands.has_permissions(kick_members=True)
    @commands.guild_only()
    @commands.cooldown(1, 2, commands.BucketType.guild)
    @commands.command(aliases=['spark'])
    async def kick(self, ctx, bruker: discord.Member, *, begrunnelse: str=None):
        """Kaster ut en bruker fra serveren"""

        await bruker.kick(reason=begrunnelse)
        await ctx.send(f'{bruker.mention} `{bruker.name}#{bruker.discriminator}` ble kastet ut av serveren')

    @commands.bot_has_permissions(ban_members=True)
    @commands.has_permissions(ban_members=True)
    @commands.guild_only()
    @commands.cooldown(1, 2, commands.BucketType.guild)
    @commands.command()
    async def ban(self, ctx, bruker: discord.Member, *, begrunnelse: str=None):
        """Utesteng en bruker fra serveren"""

        await bruker.ban(reason=begrunnelse)
        await ctx.send(f'{bruker.mention} `{bruker.name}#{bruker.discriminator}` ble utestengt fra serveren')

    @commands.bot_has_permissions(manage_messages=True)
    @commands.has_permissions(manage_messages=True)
    @commands.cooldown(1, 30, commands.BucketType.guild)
    @commands.command(aliases=['purge', 'delete', 'slett'])
    async def prune(self, ctx, antall: int):
        """Sletter de siste antall meldingene du spesifiser"""

        if antall > 100:
            return await Defaults.error_warning_send(ctx, text='Du kan ikke slette mer enn 100 meldinger om gangen')

        await ctx.channel.purge(limit=antall+1)
        await ctx.send(content=f'🗑️ Slettet `{antall}` meldinger!', delete_after=3.0)

    @commands.guild_only()
    @commands.bot_has_permissions(embed_links=True)
    @commands.cooldown(1, 2, commands.BucketType.guild)
    @commands.group()
    async def cog(self, ctx):
        """Skru av/på en cog for serveren"""

        if ctx.invoked_subcommand is None:
            await ctx.send_help(ctx.command)

    @commands.has_permissions(manage_guild=True)
    @cog.command(aliases=['disable', 'off'])
    async def av(self, ctx, cog: str):
        """Skru av cogen for serveren"""

        database_find = {'_id': ctx.guild.id}
        database_guild = self.database_col_cog_check.find_one(database_find)
        try:
            disabled = database_guild['disabled']
        except TypeError:
            self.database_col_cog_check.insert_one({'_id': ctx.guild.id, 'disabled': [cog]})
            embed = discord.Embed(description=f'✅ `{cog}` er nå skrudd **av** for serveren')
            await Defaults.set_footer(ctx, embed)
            return await ctx.send(embed=embed)
        
        disabled.append(cog)
        self.database_col_cog_check.update_one(database_find, {'$set': {'disabled': disabled}})
        embed = discord.Embed(description=f'✅ `{cog}` er nå skrudd **av** for serveren')
        await Defaults.set_footer(ctx, embed)
        await ctx.send(embed=embed)

    @commands.has_permissions(manage_guild=True)
    @cog.command(aliases=['enable', 'on'])
    async def på(self, ctx, cog: str):
        """Skru på cogen for serveren"""

        database_find = {'_id': ctx.guild.id}
        database_guild = self.database_col_cog_check.find_one(database_find)
        try:
            disabled = database_guild['disabled']
        except TypeError:
            self.database_col_cog_check.insert_one({'_id': ctx.guild.id, 'disabled': []})
            embed = discord.Embed(description=f'✅ `{cog}` er nå skrudd **på** for serveren')
            await Defaults.set_footer(ctx, embed)
            return await ctx.send(embed=embed)

        if cog in database_guild['disabled']:
            disabled.remove(cog)
            self.database_col_cog_check.update_one(database_find, {'$set': {'disabled': disabled}})
            embed = discord.Embed(description=f'✅ `{cog}` er nå skrud **på** for serveren')
            await Defaults.set_footer(ctx, embed)
            return await ctx.send(embed=embed)

        await Defaults.error_warning_send(ctx, text='Coggen finnes ikke. Sjekk om du har stor forbokstav')

    @cog.command()
    async def liste(self, ctx):
        """Se listen over avskrudde cogs"""

        database_find = {'_id': ctx.guild.id}
        database_guild = self.database_col_cog_check.find_one(database_find)
        try:
            disabled = database_guild['disabled']
        except TypeError:
            return await Defaults.error_warning_send(ctx, text='Det er ingen avskrudde cogs')
        
        if disabled == []:
            return await Defaults.error_warning_send(ctx, text='Det er ingen avskrudde cogs')

        disabled = '\n'.join(disabled)
        embed = discord.Embed(title='Avskrudde cogs', description=f'```\n{disabled}\n```')
        embed.set_author(name=ctx.guild.name, icon_url=ctx.guild.icon_url)
        await Defaults.set_footer(ctx, embed)
        await ctx.send(embed=embed)



def setup(bot):
    bot.add_cog(ServerManagement(bot))
