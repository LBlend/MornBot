from discord.ext import commands
import discord

import pymongo
from json import load as json_load
from os import remove

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

        if message.content.lower().startswith('kjære dagbok:') or message.content.lower().startswith('kjære dagbok,'):

            database_find = {'_id': message.author.id}
            database_user = database_col_dagbok.find_one(database_find)

            if database_user is None:
                return

            date = message.created_at.strftime('%d-%m-%Y')
            
            database_col_dagbok.update_one(
                database_find,
                {'$set':
                        {f'data.{date}': message.clean_content}},
                upsert=True)

            try:
                await message.add_reaction('✅')
            except:
                pass

    @commands.guild_only()
    @commands.bot_has_permissions(embed_links=True)
    @commands.cooldown(1, 2, commands.BucketType.guild)
    @commands.group()
    async def dagbok(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send_help(ctx.command)

    @dagbok.command()
    async def på(self, ctx):
        """Legger deg inn i databasen"""

        database_find = {'_id': ctx.author.id}
        database_user = database_col_dagbok.find_one(database_find)
        if database_user is not None:
            embed = discord.Embed(
                description='Du ligger allerede i databasen')
            await Defaults.set_footer(ctx, embed)
            return await ctx.send(embed=embed)

        database_col_dagbok.insert_one({'_id': ctx.author.id})
        embed = discord.Embed(
            description=':white_check_mark: Du er nå i lagt inn i databasen')
        await Defaults.set_footer(ctx, embed)
        await ctx.send(embed=embed)

    @dagbok.command()
    async def av(self, ctx):
        """Sletter deg fra databasen"""

        database_find = {'_id': ctx.author.id}
        database_user = database_col_dagbok.find_one(database_find)
        if database_user is None:
            embed = discord.Embed(
                description='Du lå ikke i databasen fra før av')
            await Defaults.set_footer(ctx, embed)
            return await ctx.send(embed=embed)

        database_col_dagbok.delete_one(database_user)

        embed = discord.Embed(
            description=':white_check_mark: Dine data har blitt slettet!')
        await Defaults.set_footer(ctx, embed)
        await ctx.send(embed=embed)

    @dagbok.command()
    async def dag(self, ctx, dato: str):
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
            embed.set_footer(
                text=f'{ctx.author.name}#{ctx.author.discriminator} | {dato}',
                icon_url=ctx.author.avatar_url)
            return await ctx.send(embed=embed)
        except:
            await Defaults.error_fatal_send(
                ctx, text='Fant ingen data fra denne datoen. Dobbelsjekk ' +
                          'om du har skrevet riktig dato `DD-MM-YYYY`',
                          mention=False)

    @dagbok.command()
    async def data(self, ctx):
        """Sender deg dine data"""

        database_find = {'_id': ctx.author.id}
        database_user = database_col_dagbok.find_one(database_find)

        if database_user is None:
            return await Defaults.error_warning_send(
                ctx, text='Jeg har ingen data om deg')
            
        raw_data = ''
        try:
            database_user['data']
        except KeyError:
            return await Defaults.error_warning_send(
                ctx, text='Jeg har ingen data om deg')

        for key, value in database_user['data'].items():
            raw_data += f'({key})\n{value}\n\n'

        with open(f'./assets/{ctx.author.id}.txt',
                  'a+', encoding='utf-8') as f:
            f.write(raw_data)

        try:
            await ctx.author.send(
                file=discord.File(f'./assets/{ctx.author.id}.txt'))
            embed = discord.Embed(
                color=0x0085ff,
                description=':white_check_mark: Dine data har ' +
                            'blitt sendt i DM!')
        except:
            await Defaults.error_fatal_send(
                ctx,
                text='Sending av data feilet! Sjekk om du har blokkert meg')

        await Defaults.set_footer(ctx, embed)
        await ctx.send(embed=embed)

        try:
            remove(f'./assets/{ctx.author.id}.txt')
        except:
            pass


def setup(bot):
    bot.add_listener(Dagbok(bot).react, 'on_message')
    bot.add_cog(Dagbok(bot))