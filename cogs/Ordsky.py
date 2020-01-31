import discord
from discord.ext import commands

from codecs import open
import json

from PIL import Image
from numpy import array
from wordcloud import WordCloud
from re import sub
from os import remove
import functools
from io import BytesIO

from cogs.utils import Defaults


class Ordsky(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @staticmethod
    def generate(text, mask, filtered_words):
        """Generate wordcloud"""

        wc = WordCloud(max_words=4000, mask=mask, repeat=False, stopwords=filtered_words)
        wc.process_text(text)
        wc.generate(text)
        img = wc.to_image()
        b = BytesIO()
        img.save(b, 'png')
        b.seek(0)
        return b

    @commands.bot_has_permissions(embed_links=True)
    @commands.group()
    async def ordsky(self, ctx):
        """Generer en ordsky basert på meldingene dine"""

        if ctx.invoked_subcommand is None:
            await self.generer.invoke(ctx)

    @commands.cooldown(1, 2, commands.BucketType.user)
    @ordsky.command(aliases=['consent'])
    async def samtykke(self, ctx):
        """Gi samtykke til å samle meldingsdataen din"""

        database_find = {'_id': ctx.author.id}
        try:
            database_user = self.bot.database['ordsky'].find_one(database_find)
        except:
            return await Defaults.error_fatal_send(ctx, text='Jeg har ikke tilkobling til databasen\n\n' +
                                                             'Be båtteier om å fikse dette')

        if database_user is None:
            self.bot.database['ordsky'].insert_one({'_id': ctx.author.id, 'ordsky_consent': False})
            self.bot.database['ordsky'].find_one(database_find)
            self.bot.database['ordsky'].update_one(database_find, {'$set': {'ordsky_consent': True}})
        else:
            self.bot.database['ordsky'].update_one(database_find, {'$set': {'ordsky_consent': True}})

        embed = discord.Embed(color=ctx.me.color, description='✅ Samtykke registrert!')
        await Defaults.set_footer(ctx, embed)
        await ctx.send(embed=embed)

    @commands.cooldown(1, 2, commands.BucketType.user)
    @ordsky.command(aliases=['ingensamtykke', 'noconsent', 'slettdata'])
    async def tabort(self, ctx):
        """Fjern samtykke og slett meldingsdata"""

        database_find = {'_id': ctx.author.id}
        try:
            database_user = self.bot.database['ordsky'].find_one(database_find)
        except:
            return await Defaults.error_fatal_send(ctx, text='Jeg har ikke tilkobling til databasen\n\n' +
                                                             'Be båtteier om å fikse dette')

        self.bot.database['ordsky'].delete_one(database_user)

        embed = discord.Embed(color=ctx.me.color, description='✅ Meldingsdata er slettet!')
        await Defaults.set_footer(ctx, embed)
        await ctx.send(embed=embed)

    @commands.cooldown(1, 60, commands.BucketType.user)
    @ordsky.command(aliases=['mydata'])
    async def data(self, ctx):
        """Få tilsendt dine data"""

        database_find = {'_id': ctx.author.id}
        try:
            database_user = self.bot.database['ordsky'].find_one(database_find)
        except:
            return await Defaults.error_fatal_send(ctx, text='Jeg har ikke tilkobling til databasen\n\n' +
                                                             'Be båtteier om å fikse dette')

        if database_user is None:
            self.bot.database['ordsky'].insert_one({'_id': ctx.author.id, 'ordsky_consent': False})
            return await Defaults.error_warning_send(ctx, text='Jeg har ingen data om deg å sende eller ' +
                                                               'så kan jeg ikke sende meldinger til deg!')

        try:
            database_user['ordsky_data']
        except KeyError:
            return await Defaults.error_warning_send(ctx, text='Jeg har ingen data om deg å sende eller ' +
                                                               'så kan jeg ikke sende meldinger til deg!')

        raw_data = ''
        for value in database_user['ordsky_data'].values():
            if value is None:
                continue
            else:
                raw_data += value

        if raw_data == '':
            return await Defaults.error_warning_send(ctx, text='Jeg har ingen data om deg å sende eller ' +
                                                               'så kan jeg ikke sende meldinger til deg!')

        with open(f'./assets/temp/{ctx.author.id}_ordsky.json', 'w') as f:
            json.dump(database_user, f, indent=4)

        try:
            await ctx.author.send(file=discord.File(f'./assets/temp/{ctx.author.id}_ordsky.json'))
            embed = discord.Embed(color=ctx.me.color, description='✅ Meldingsdata har blitt sendt i DM!')
            await Defaults.set_footer(ctx, embed)
            await ctx.send(embed=embed)
        except:
            await Defaults.error_fatal_send(ctx, text='Sending av data feilet! Sjekk om du har blokkert meg')

        try:
            remove(f'./assets/temp/{ctx.author.id}_ordsky.json')
        except:
            pass

    @commands.bot_has_permissions(embed_links=True, read_message_history=True, attach_files=True)
    @commands.cooldown(1, 150, commands.BucketType.user)
    @ordsky.command(aliases=['generate', 'create', 'lag'])
    async def generer(self, ctx):
        """Generer en ordsky"""

        database_find = {'_id': ctx.author.id}
        try:
            database_user = self.bot.database['ordsky'].find_one(database_find)
        except:
            return await Defaults.error_fatal_send(ctx, text='Jeg har ikke tilkobling til databasen\n\n' +
                                                             'Be båtteier om å fikse dette')

        if database_user is None:
            self.bot.database['ordsky'].insert_one({'_id': ctx.author.id, 'ordsky_consent': False})
            self.bot.database['ordsky'].find_one(database_find)

        database_user = self.bot.database['ordsky'].find_one(database_find)

        if database_user['ordsky_consent'] is False:
            await Defaults.error_warning_send(ctx, text='Du må gi meg tillatelse til å samle og beholde ' +
                                                        'meldingsdataene dine.\n\n' +
                                                        f'Skriv `{self.bot.prefix}ordsky samtykke` for å gjøre dette',
                                              mention=True)
            self.bot.get_command(f'{ctx.command}').reset_cooldown(ctx)            
            return 

        embed = discord.Embed(description='**Henter meldinger:** ⌛\n**Generer ordsky:** -')
        await Defaults.set_footer(ctx, embed)
        status_msg = await ctx.send(embed=embed)

        command_prefixes = ['§', '!', '.', '-', '€', '|', '$', '=', '?', '<', ':', '#', ',']

        message_data = ''
        try:
            database_user['ordsky_data'][f'{ctx.guild.id}']
            for channel in ctx.guild.text_channels:
                if not channel.permissions_for(ctx.author).send_messages:
                    continue
                try:
                    async for message in channel.history(limit=300):
                        has_prefixes = False
                        if message.author.id == ctx.author.id:
                            for prefixes in command_prefixes:
                                if prefixes in message.clean_content[:3]:
                                    has_prefixes = True
                            if has_prefixes is False:
                                message_data += f'[{str(message.created_at)[0:19]}] ' +\
                                                f'({message.channel.id}-{message.id}) ' +\
                                                f'{message.clean_content} '
                except:
                    continue

        except KeyError:
            for channel in ctx.guild.text_channels:
                if not channel.permissions_for(ctx.author).send_messages:
                    continue
                try:
                    async for message in channel.history(limit=2000):
                        has_prefixes = False
                        if message.author.id == ctx.author.id:
                            for prefixes in command_prefixes:
                                if prefixes in message.clean_content[:3]:
                                    has_prefixes = True
                            if has_prefixes is False:
                                message_data += f'[{str(message.created_at)[0:19]}] ' +\
                                                f'({message.channel.id}-{message.id}) ' +\
                                                f'{message.clean_content} '
                except:
                    continue
        if message_data != '':
            self.bot.database['ordsky'].update_one(database_find,
            {'$set': {f'ordsky_data.{ctx.guild.id}': message_data}}, upsert=True)

        database_user = self.bot.database['ordsky'].find_one(database_find)
        try:
            message_data = database_user['ordsky_data'][f'{ctx.guild.id}']
        except KeyError:
            return await Defaults.error_fatal_edit(ctx, status_msg,
                                                   text='Har ikke nok meldingsdata for å generere ordsky')

        database_message_data = message_data

        embed = discord.Embed(description='**Henter meldinger:** ✅\n**Generer ordsky:** ⌛')
        await Defaults.set_footer(ctx, embed)
        await status_msg.edit(embed=embed)

        text = sub(r'http\S+', '', database_message_data)
        text = sub(r':\S+', '', text)
        text = sub(r'#\S+', '', text)
        text = sub(r'@\S+', '', text)

        with open('./assets/ordsky/ordliste.txt', 'r', encoding='utf-8') as f:
            filtered_words = [line.split(',') for line in f.readlines()]
            filtered_words = filtered_words[0]

        mask = array(Image.open('./assets/ordsky/mask/skyform.png'))

        task = functools.partial(Ordsky.generate, text, mask, filtered_words)
        b = await self.bot.loop.run_in_executor(None, task)

        if str(ctx.author.color) != '#000000':
            color = ctx.author.color
        else:
            color = discord.Colour(0x99AAB5)

        final_image = discord.File(b, filename=f'{ctx.author.id}_{ctx.guild.id}.png')
        embed = discord.Embed(color=color, description='☁️ Her er ordskyen din! ☁️')
        embed.set_image(url=f'attachment://{ctx.author.id}_{ctx.guild.id}.png')
        await Defaults.set_footer(ctx, embed)
        await ctx.send(file=final_image, content=ctx.author.mention, embed=embed)

        await status_msg.delete()


def setup(bot):
    bot.add_cog(Ordsky(bot))
