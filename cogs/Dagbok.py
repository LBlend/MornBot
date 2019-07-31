from discord.ext import commands
import discord

import pymongo
from json import load as json_load
from os import remove
from math import ceil
import json
import asyncio

from cogs.utils import Defaults

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
            
            database_col_dagbok.update_one(database_find,
                                           {'$set': {f'data.{date}': message.clean_content}}, upsert=True)

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
            embed = discord.Embed(description='Du ligger allerede i databasen')
            await Defaults.set_footer(ctx, embed)
            return await ctx.send(embed=embed)

        database_col_dagbok.insert_one({'_id': ctx.author.id})
        embed = discord.Embed(description=':white_check_mark: Du er nå i lagt inn i databasen')
        await Defaults.set_footer(ctx, embed)
        await ctx.send(embed=embed)

    @dagbok.command()
    async def av(self, ctx):
        """Sletter deg fra databasen"""

        database_find = {'_id': ctx.author.id}
        database_user = database_col_dagbok.find_one(database_find)
        if database_user is None:
            embed = discord.Embed(description='Du lå ikke i databasen fra før av')
            await Defaults.set_footer(ctx, embed)
            return await ctx.send(embed=embed)

        embed = discord.Embed(color=ctx.me.color, description='Er du sikker? Reager med ✅ innen 30s har gått for å ' +
                                                              'bekrefte\n\n**Dette vil slette alle dine data og ' +
                                                              'stoppe loggingen av fremtidige meldinger frem til du ' +
                                                              'skrur den på igjen.** Om du vil hente ut data før du ' +
                                                              f'sletter, kan du skrive `{prefix}dagbok data`')
        confirmation_msg = await ctx.send(embed=embed)
        await confirmation_msg.add_reaction('✅')

        def comfirm(reaction, user):
            return user == ctx.author and str(reaction.emoji) == '✅'

        try:
            reaction, user = await self.bot.wait_for('reaction_add', timeout=30.0, check=comfirm)
        except asyncio.TimeoutError:
            embed = discord.Embed(color=ctx.me.color, description=f'Ingen svar ble gitt innen tiden!')
            await confirmation_msg.edit(embed=embed)
            await confirmation_msg.remove_reaction('✅', ctx.me)
        else:
            database_col_dagbok.delete_one(database_user)
            embed = discord.Embed(description=':white_check_mark: Dine data har blitt slettet!')
            await Defaults.set_footer(ctx, embed)
            await ctx.send(embed=embed)

    @dagbok.command()
    async def liste(self, ctx, *side: int):
        """Se hvilke dager som ligger i dagboka"""

        database_find = {'_id': ctx.author.id}
        database_user = database_col_dagbok.find_one(database_find)

        if str(ctx.author.color) != '#000000':
            color = ctx.author.color
        else:
            color = discord.Colour(0x99AAB5)

        if database_user is None:
            return await Defaults.error_warning_send(ctx, text='Du ligger ikke i databasen. ' +
                                                               f'Skriv `{prefix}dagbok på` for å legge deg inn')

        try:
            entries = list(database_user['data'].keys())
        except KeyError:
            return await Defaults.error_fatal_send(ctx, text='Fant ingen data. Sørg for at du skriver en ' +
                                                             'dagboksmelding først (start melding med `kjære dagbok,`',)

        if side is ():
            side = 1
        else:
            side = side[0]

        if side <= 0:
            side = 1

        start_index = (side - 1) * 10
        end_index = side * 10

        pagecount = ceil(len(entries) / 10)

        if side > pagecount:
            return await Defaults.error_fatal_send(ctx, text='Ugyldig sidetall')

        entries = '\n'.join(entries[start_index:end_index])

        embed = discord.Embed(color=color, description=f'```\n{entries}\n```')
        embed.set_author(name=f'{ctx.author.name}#{ctx.author.discriminator}', icon_url=ctx.author.avatar_url)
        embed.set_footer(text=f'Side: {side}/{pagecount}')
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
            return await Defaults.error_warning_send(ctx, text='Du ligger ikke i databasen. ' +
                                                               f'Skriv `{prefix}dagbok på` for å legge deg inn')
        try:
            data = database_user['data'][f'{dato}']
            embed = discord.Embed(color=color, description=data)
            embed.set_footer(text=f'{ctx.author.name}#{ctx.author.discriminator} | {dato}',
                             icon_url=ctx.author.avatar_url)
            return await ctx.send(embed=embed)
        except:
            await Defaults.error_fatal_send(ctx, text='Fant ingen data fra denne datoen. Dobbelsjekk ' +
                                                      'om du har skrevet riktig dato `DD-MM-YYYY`')

    @dagbok.command()
    async def data(self, ctx):
        """Sender deg dine data"""

        database_find = {'_id': ctx.author.id}
        database_user = database_col_dagbok.find_one(database_find)

        if database_user is None:
            return await Defaults.error_warning_send(ctx, text='Jeg har ingen data om deg')

        try:
            database_user['data']
        except KeyError:
            return await Defaults.error_warning_send(ctx, text='Jeg har ingen data om deg')

        with open(f'./assets/{ctx.author.id}.json', 'w') as f:
            json.dump(database_user, f, indent=4)

        try:
            await ctx.author.send(file=discord.File(f'./assets/{ctx.author.id}.json'))
            embed = discord.Embed(color=0x0085ff, description=':white_check_mark: Dine data har ' +
                                                              'blitt sendt i DM!')
            await ctx.send(embed=embed)
        except:
            await Defaults.error_fatal_send(ctx, text='Sending av data feilet! Sjekk om du har blokkert meg')

        try:
            remove(f'./assets/{ctx.author.id}.txt')
        except:
            pass


def setup(bot):
    bot.add_listener(Dagbok(bot).react, 'on_message')
    bot.add_cog(Dagbok(bot))