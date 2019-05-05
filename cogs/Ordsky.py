import discord
import asyncio
from discord.ext import commands

import pymongo

import codecs
from json import load as json_load

from PIL import Image
from numpy import array
from wordcloud import WordCloud
from re import sub
from os import remove
import functools
from io import BytesIO

# Hent prefiks og monogdb innlogging
with codecs.open('config.json', 'r', encoding='utf8') as f:
    config = json_load(f)
    prefix = config['prefix']
    mongodb_url = config['mongodb_url']

# Koble til database
mongo = pymongo.MongoClient(mongodb_url)
database = mongo['discord']
database_col_users = database['users']

async def default_db_insert(self, ctx):
    """Standardmal for ny bruker i database"""
    database_col_users.insert_one(
        {'_id': ctx.author.id,
         'ordsky_consent': False,
         'ordsky_data': {f'{ctx.guild.id}': None}})

async def error_no_data(self, ctx):
    """Send standard feilmelding for ingen data"""
    embed = discord.Embed(
        color=0xF1C40F,
        description=':exclamation: Jeg har ingen data om deg å ' +
                    'sende eller så kan jeg ikke sende meldinger til deg!')
    embed.set_footer(icon_url=ctx.author.avatar_url,
                     text=f'{ctx.author.name}#{ctx.author.discriminator}')
    await ctx.send(embed=embed)


class Ordsky(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @staticmethod
    def generate(text, mask_bilde, filtered_words):
        """Generer ordsky"""
        wc = WordCloud(font_path=None,
                       max_words=4000,
                       mask=mask_bilde,
                       repeat=True,
                       stopwords=filtered_words)
        wc.process_text(text)
        wc.generate(text)
        img = wc.to_image()
        b = BytesIO()
        img.save(b, 'png')
        b.seek(0)
        return b

    @commands.cooldown(1, 2, commands.BucketType.user)
    @commands.command(aliases=['consent'])
    async def samtykke(self, ctx):
        """Gi samtykke til å samle meldingsdataen din"""

        # Let i database etter bruker
        database_find = {'_id': ctx.author.id}
        try:
            database_user = database_col_users.find_one(database_find)
        except:
            await ctx.send(f'{ctx.author.mention} Jeg har ikke ' +
                            'tilkobling til databasen. ' +
                            'Be boteier om å fikse dette')
            return

        # Sett inn manglende data i database og sett samtykke
        if database_user is None:
            await default_db_insert(self, ctx)
        else:
            database_col_users.update_one(database_find,
                                          {'$set':
                                           {'ordsky_consent': True}})

        # Send bekreftelsesmelding
        embed = discord.Embed(
            color=0x0085ff,
            description=':white_check_mark: Samtykke registrert!')
        embed.set_footer(icon_url=ctx.author.avatar_url,
                         text=f'{ctx.author.name}#{ctx.author.discriminator}')
        await ctx.send(embed=embed)

    @commands.cooldown(1, 2, commands.BucketType.user)
    @commands.command(aliases=['ingensamtykke', 'noconsent', 'slettdata'])
    async def tabort(self, ctx):
        """Fjern samtykke og slett meldingsdata"""

        # Let i database etter bruker
        database_find = {'_id': ctx.author.id}
        try:
            database_user = database_col_users.find_one(database_find)
        except:
            await ctx.send(f'{ctx.author.mention} Jeg har ikke ' +
                            'tilkobling til databasen. ' +
                            'Be boteier om å fikse dette')
            return

        # Sett inn manglende data i database/fjern samtykke og meldingsdata
        if database_user is None:
            await default_db_insert(self, ctx)
        else:
            database_col_users.update_one(database_find,
                                          {'$set':
                                           {'ordsky_consent': False}})
            for guild in database_user['ordsky_data']:
                database_col_users.update_one(database_find,
                                              {'$set':
                                               {f'ordsky_data.{guild}': None}},
                                              upsert=True)

        # Send bekreftelsesmelding
        embed = discord.Embed(
            color=0x0085ff,
            description=':white_check_mark: Meldingsdata er slettet!')
        embed.set_footer(icon_url=ctx.author.avatar_url,
                         text=f'{ctx.author.name}#{ctx.author.discriminator}')
        await ctx.send(embed=embed)

    @commands.cooldown(1, 60, commands.BucketType.user)
    @commands.command(aliases=['mydata'])
    async def minedata(self, ctx):
        '''Få tilsendt dine data'''

        # Let i database etter bruker
        database_find = {'_id': ctx.author.id}
        try:
            database_user = database_col_users.find_one(database_find)
        except:
            await ctx.send(f'{ctx.author.mention} Jeg har ikke ' +
                            'tilkobling til databasen. ' +
                            'Be boteier om å fikse dette')
            return

        # Sett inn manglende data i database og send melding om ingen data
        if database_user is None:
            await default_db_insert(self, ctx)
            await error_no_data(self, ctx)
            return

        # Hent data fra alle guilds og samle i string
        raw_data = ''
        for key, value in database_user['ordsky_data'].items():
            if value is None:
                continue
            else:
                raw_data += value

        # Feilmelding om ingen meldingsdata er funnet
        if raw_data == '':
            await error_no_data(self, ctx)
            return

        # Legg meldingsdata inn i tekstfil
        with codecs.open(f'./assets/ordsky/{ctx.author.id}.txt',
                         'a+', encoding='utf-8') as f:
            f.write(raw_data)

        # Send tekstfil
        try:
            await ctx.author.send(
                file=discord.File(f'./assets/ordsky/{ctx.author.id}.txt'))
            embed = discord.Embed(
                color=0x0085ff,
                description=':white_check_mark: Meldingsdata har ' +
                            'blitt sendt i DM!')
        except:
            embed = discord.Embed(
                color=0xFF0000,
                description=':x: Sending av data feilet! ' +
                            'Sjekk om du har blokkert meg')
        embed.set_footer(
            icon_url=ctx.author.avatar_url,
            text=f'{ctx.author.name}#{ctx.author.discriminator}')
        await ctx.send(embed=embed)

        # Slett den lokale tekstfilen
        try:
            remove(f'./assets/ordsky/{ctx.author.id}.txt')
        except:
            pass

    @commands.cooldown(1, 150, commands.BucketType.user)
    @commands.command(aliases=['wordcloud', 'wc', 'sky'])
    async def ordsky(self, ctx):
        """Generer en ordsky"""

        # Let i database etter bruker
        database_find = {'_id': ctx.author.id}
        try:
            database_user = database_col_users.find_one(database_find)
        except:
            await ctx.send(f'{ctx.author.mention} Jeg har ikke ' +
                            'tilkobling til databasen. ' +
                            'Be boteier om å fikse dette')
            return

        # Sett inn manglende data i database
        if database_user is None:
            await default_db_insert(self, ctx)
            database_user = database_col_users.find_one(database_find)
        if ctx.guild.id not in database_user['ordsky_data']:
            database_col_users.update_one(
                database_find,
                {'$set':
                 {f'ordsky_data.{ctx.guild.id}': None}},
                upsert=True)

        # Let i database på nytt for opddaterte verdier
        database_user = database_col_users.find_one(database_find)

        # Sjekk om bruker har gitt samtykke
        if database_user['ordsky_consent'] is False:
            embed = discord.Embed(
                color=0xF1C40F,
                description=':exclamation: Du må gi meg tillatelse til å ' +
                            'samle og beholde meldingsdataene dine.\n\n' +
                            f'Skriv `{prefix}samtykke` for å gjøre dette')
            embed.set_footer(
                icon_url=ctx.author.avatar_url,
                text=f'{ctx.author.name}#{ctx.author.discriminator}')
            status_msg = await ctx.send(ctx.author.mention, embed=embed)
            self.bot.get_command('ordsky').reset_cooldown(ctx)
            return

        # Statusmelding
        embed = discord.Embed(
            description='**Henter meldinger:** :hourglass:\n' +
                        '**Generer ordsky:** -')
        embed.set_footer(
            icon_url=ctx.author.avatar_url,
            text=f'{ctx.author.name}#{ctx.author.discriminator}')
        status_msg = await ctx.send(embed=embed)

        # Hent meldinger
        message_data = ''
        if database_user['ordsky_data'][f'{ctx.guild.id}'] is None:
            for channel in ctx.guild.text_channels:
                try:
                    async for message in channel.history(limit=2000):
                        if message.author.id == ctx.author.id:
                            message_data += f'{message.clean_content} '
                except:
                    continue
            database_col_users.update_one(
                database_find,
                {'$set':
                 {f'ordsky_data.{ctx.guild.id}': message_data}},
                upsert=True)
            database_message_data = message_data

        else:
            for channel in ctx.guild.text_channels:
                try:
                    async for message in channel.history(limit=300):
                        if message.author.id == ctx.author.id:
                            message_data += f'{message.clean_content} '
                except:
                    continue
            database_message_data = database_user['ordsky_data']
            [f'{ctx.guild.id}']
            database_message_data += message_data
            database_col_users.update_one(
                database_find,
                {'$set':
                 {f'ordsky_data.{ctx.guild.id}': database_message_data}},
                upsert=True)

        # Rediger statusmelding. Fortell at meldingshenting er ferdig
        embed = discord.Embed(
            description='**Henter meldinger:** :white_check_mark:\n' +
                        '**Generer ordsky:** :hourglass:')
        embed.set_footer(
            icon_url=ctx.author.avatar_url,
            text=f'{ctx.author.name}#{ctx.author.discriminator}')
        await status_msg.edit(embed=embed)

        # Lenkefiltrering i meldingsdata
        text = sub(r'http\S+', '', database_message_data)

        # Hent ordliste for filtrering
        with codecs.open('./assets/ordsky/ordliste.txt', 'r') as f:
            filtered_words = [line.split(',') for line in f.readlines()]
            filtered_words = filtered_words[0]

        # Hent skyform/mask
        mask_bilde = array(Image.open('./assets/ordsky/mask/skyform.png'))

        task = functools.partial(
            Ordsky.generate, text,
            mask_bilde, filtered_words)
        b = await self.bot.loop.run_in_executor(None, task)

        # Sett embedfarge
        if str(ctx.author.color) != '#000000':
            color = ctx.author.color
        else:
            color = discord.Colour(0x99AAB5)

        # Lag embed og send
        final_image = discord.File(
            b, filename=f'{ctx.author.id}_{ctx.guild.id}.png')
        embed = discord.Embed(
            color=color,
            description=':cloud: Her er ordskyen din! :cloud:')
        embed.set_image(url=f'attachment://{ctx.author.id}_{ctx.guild.id}.png')
        embed.set_footer(
            text=f'{ctx.author.name}#{ctx.author.discriminator}',
            icon_url=ctx.author.avatar_url)
        await ctx.send(
            file=final_image,
            content=ctx.author.mention,
            embed=embed)

        # Slett statusmelding
        await status_msg.delete()


def setup(bot):
    bot.add_cog(Ordsky(bot))
