from discord.ext import commands
import discord

import pymongo
from json import load as json_load

from .utils import Defaults

with open('config.json', 'r', encoding='utf8') as f:
    config = json_load(f)
    prefix = config['prefix']
    mongodb_url = config['mongodb_url']

mongo = pymongo.MongoClient(mongodb_url)
database = mongo['discord']
database_col_dagbok = database['dagbok']


class Dagbok(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def react(self, message):
        if message.author.bot:
            return

        if message.content.lower().startswith('kjære dagbok:'):

            database_find = {'_id': message.author.id}
            database_user = database_col_dagbok.find_one(database_find)

            if database_user is None:
                return

            date = message.created_at.strftime('%d-%m-%Y')

            try:
                database_user['data'][f'{date}']
            except:
                database_col_dagbok.update_one(
                    database_find,
                    {'$set':
                         {f'data.{date}': message.clean_content}},
                    upsert=True)

    @commands.guild_only()
    @commands.bot_has_permissions(embed_links=True)
    @commands.cooldown(1, 2, commands.BucketType.guild)
    @commands.command()
    async def mindagbok(self, ctx, dato: str):
        """Hent opp dagboka di fra en dato"""

        database_find = {'_id': ctx.author.id}
        database_user = database_col_dagbok.find_one(database_find)

        if str(ctx.author.color) != '#000000':
            color = ctx.author.color
        else:
            color = discord.Colour(0x99AAB5)

        if database_user is None:
            return await Defaults.error_warning_send(
                ctx, text='Du ligger ikke i databasen. Skriv ' +
                          f'`{prefix}dagbok på` for å legge deg inn')
        try:
            data = database_user['data'][f'{dato}']
            embed = discord.Embed(
                color=color, description=data)
            await Defaults.set_footer(ctx, embed)
            return await ctx.send(embed=embed)
        except:
            await Defaults.error_fatal_send(
                ctx, text='Fant ingen data fra denne datoen. Dobbelsjekk ' +
                          'om du har skrevet riktig dato `DD-MM-YYYY`')

    @commands.guild_only()
    @commands.bot_has_permissions(embed_links=True)
    @commands.cooldown(1, 2, commands.BucketType.guild)
    @commands.group()
    async def dagbok(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send_help(ctx.command)

    @dagbok.command()
    async def på(self, ctx):
        """legger deg i database"""

        database_col_dagbok.insert_one({'_id': ctx.author.id})
        await ctx.send('Du er nå lagt inn i databasen!')

    @dagbok.command()
    async def av(self, ctx):
        """Sletter deg fra database"""

        database_find = {'_id': ctx.author.id}
        database_user = database_col_dagbok.find_one(database_find)
        database_col_dagbok.delete_one(database_user)

        await ctx.send(
            'Du er nå fjernet fra databasen. All din data er slettet')


def setup(bot):
    bot.add_listener(Dagbok(bot).react, 'on_message')
    bot.add_cog(Dagbok(bot))