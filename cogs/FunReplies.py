from discord.ext import commands
import discord


class FunReplies(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    @commands.bot_has_permissions(embed_links=True)
    @commands.cooldown(1, 2, commands.BucketType.guild)
    @commands.group()
    async def funreplies(self, ctx):
        """Skru av/på responser som ikke krever prefiks"""

        if ctx.invoked_subcommand is None:
            await ctx.send_help(ctx.command)

    @funreplies.command()
    async def on(self, ctx, *, kanal: discord.TextChannel=None):
        """Skrur på funreplies for spesifisert kanal"""

        if not kanal:
            kanal = ctx.channel

        database_find = {'_id': kanal.id}
        try:
            database_funreplies = self.bot.database['funreplies'].find_one(database_find)
        except:
            return await ctx.send(f'{ctx.author.mention} Jeg har ikke tilkobling til databasen. ' +
                                  f'Be boteier om å fikse dette')

        try:
            database_funreplies[f'{kanal.id}']
        except TypeError:
            self.bot.database['funreplies'].insert_one({'_id': kanal.id, 'funreplies': True})

        embed = discord.Embed(color=ctx.me.color, description=f'FunReplies er nå skrudd **på** for {kanal.mention}')
        await ctx.send(embed=embed)

    @funreplies.command()
    async def off(self, ctx, *, kanal: discord.TextChannel = None):
        """Skrur av funreplies for spesifisert kanal"""

        if not kanal:
            kanal = ctx.channel

        database_find = {'_id': kanal.id}
        try:
            database_funreplies = self.bot.database['funreplies'].find_one(database_find)
        except:
            return await ctx.send(f'{ctx.author.mention} Jeg har ikke tilkobling til databasen. ' +
                                  'Be boteier om å fikse dette')

        self.bot.database['funreplies'].delete_one(database_funreplies)

        embed = discord.Embed(color=ctx.me.color, description=f'FunReplies er nå skrudd **av** for {kanal.mention}')
        await ctx.send(embed=embed)

    async def react(self, message):
        if message.author.bot:
            return

        database_find = {'_id': message.channel.id}
        channel = self.bot.database['funreplies'].find_one(database_find)
        try:
            if not channel['funreplies']:
                return
        except TypeError:
            return

        if message.content.lower() == 'morn':
            await message.channel.send('Morn')

        elif message.content.lower() == 'no u':
            await message.channel.send(f'no u {message.author.mention}')

        elif message.content.lower() == 'nei du':
            await message.channel.send(f'nei du {message.author.mention}')


def setup(bot):
    bot.add_listener(FunReplies(bot).react, 'on_message')
    bot.add_cog(FunReplies(bot))
