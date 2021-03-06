"""
Spaghetti <3
"""


from discord.ext import commands
import discord

import locale

from requests import get
from datetime import datetime

from cogs.utils import Defaults


locale.setlocale(locale.LC_ALL, '')


class Corona(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.bot_has_permissions(embed_links=True)
    @commands.group(aliases=['korona'])
    async def corona(self, ctx):
        """Viser status for Koronaviruset"""

        if ctx.invoked_subcommand is None:
            embed = discord.Embed(color=0xFF9C00)
            embed.description = 'Grunnet en scuffed API for globale data så har denne kommandoen blitt dedikert til' +\
                                ' å vise alle de andre kommandoene.\n\nOm du likevel vil ha global statistikk så ' +\
                                f'kan du skrive:\n`{self.bot.prefix}corona verden`\n\nAndre kommandoer:\n' +\
                                f'`{self.bot.prefix}corona norge [døde]`\n' +\
                                f'`{self.bot.prefix}corona kommune <kommunenavn>`\n' +\
                                f'`{self.bot.prefix}corona alder`'
            await Defaults.set_footer(ctx, embed)
            await ctx.send(embed=embed)

    @commands.cooldown(1, 5, commands.BucketType.guild)
    @corona.command(aliases=['global'])
    async def verden(self, ctx):
        """Viser antall døde/smittede/friskmeldte globalt"""

        async with ctx.channel.typing():

            try:
                url = 'https://services1.arcgis.com/0MSEUqKaxRlEPj5g/arcgis/rest/services/ncov_cases/FeatureServer' +\
                      '/1/query?f=json&where=1%3D1&returnGeometry=false&spatialRel=esriSpatialRelIntersects&outSta' +\
                      'tistics=%5B%7B%22statisticType%22%3A%22sum%22%2C%22onStatisticField%22%3A%22Confirmed%22%2C' +\
                      '%22outStatisticFieldName%22%3A%22confirmed%22%7D%2C%20%7B%22statisticType%22%3A%22sum%22%2C' +\
                      '%22onStatisticField%22%3A%22Deaths%22%2C%22outStatisticFieldName%22%3A%22deaths%22%7D%2C%20' +\
                      '%7B%22statisticType%22%3A%22sum%22%2C%22onStatisticField%22%3A%22Recovered%22%2C%22outStati' +\
                      'sticFieldName%22%3A%22recovered%22%7D%5D&outSR=102100&cacheHint=false'
                data = get(url).json()
                infected = locale.format_string('%d', data['features'][0]['attributes']['confirmed'], grouping=True)
                dead = locale.format_string('%d', data['features'][0]['attributes']['deaths'], grouping=True)
                recovered = locale.format_string('%d', data['features'][0]['attributes']['recovered'], grouping=True)
            except:
                return await Defaults.error_fatal_send(ctx, text='Kunne ikke hente data\nAPIen er trash\n\nSkriv ' +
                                                                 f'`{self.bot.prefix}help corona` for mer statistikk')

            embed = discord.Embed(color=0xFF9C00, title='Koronaviruset - Globalt')
            embed.set_author(name='Johns Hopkins University', icon_url='https://i.forbesimg.com/media/lists/' +
                                                                       'colleges/johns-hopkins-university_41' +
                                                                       '6x416.jpg')
            embed.description = '*Dataene er samlet inn av [Johns Hopkins University]' +\
                                '(https://github.com/CSSEGISandData/COVID-19)*\n'
            embed.add_field(name='Smittede', value=infected)
            embed.add_field(name='Døde', value=dead)
            embed.add_field(name='Friskmeldte', value=recovered)
            await Defaults.set_footer(ctx, embed)
            await ctx.send(embed=embed)

    @commands.cooldown(1, 5, commands.BucketType.guild)
    @corona.command(aliases=['noreg', 'norway', 'fylker', 'counties'])
    async def norge(self, ctx, *, tilstand: str='smittede'):
        """Viser status i Norge fordelt på fylker"""

        conditions = {
            'smittede': 'confirmed',
            'døde': 'dead',
        }
        if tilstand is not None and tilstand.lower() in conditions:
            description_str = f'***{tilstand.title()}** i Norge fordelt på fylker.\n' +\
                            'Dataene er hentet fra ' +\
                            '[VG](https://www.vg.no/spesial/2020/corona-viruset/)*\n' +\
                            f'Sist oppdatert: '
            tilstand = conditions[tilstand]
        else:
            return await Defaults.error_warning_send(ctx, text='Du må velge en av følgende:\n\n' +
                                                               f'• `{self.bot.prefix}corona norge smittede`\n' +
                                                               f'• `{self.bot.prefix}corona norge døde`\n')

        async with ctx.channel.typing():

            try:
                url = 'https://redutv-api.vg.no/corona/v1/sheets/norway-table-overview/?region=county'
                data = get(url).json()
                counties = []

                # Too lazy to do it any other way rn
                timestamp = data['updated']['ts'].replace('T', '')[:-6]
                timestamp = datetime.strptime(timestamp, '%Y-%m-%d%H:%M:%S')
                timestamp = timestamp.strftime('%H:%M %d.%m.%Y')

                description_str = description_str + timestamp + '\n\n'
                for county in data['cases']:
                    counties.append(county)

                def sortinfected(x):
                    return x['confirmed']

                def sortdead(x):
                    return x['dead']

                if tilstand == 'confirmed':
                    counties.sort(key=sortinfected)
                    today = data['totals']['changes']['newToday']
                elif tilstand == 'dead':
                    counties.sort(key=sortdead)
                    today = data['totals']['changes']['deathsToday']
                counties.reverse()

                for county in counties:
                    description_str += f'**{county["name"]}**: ' +\
                                        f'{locale.format_string("%d", county[tilstand], grouping=True)}\n'

                description_str += '\n**TOTALT**: ' +\
                                    f'{locale.format_string("%d", data["totals"][tilstand], grouping=True)}'
                description_str += '\n\n**I dag**: ' +\
                                    f'{locale.format_string("%d", today, grouping=True)}'

                data = get('https://redutv-api.vg.no/corona/v1/areas/country/reports?include=hospitals').json()
                hospitalized = data['hospitals']['total']['hospitalized']
                respiratory = data['hospitals']['total']['respiratory']
                description_str += '\n**Innlagte**: ' +\
                                    f'{locale.format_string("%d", hospitalized, grouping=True)}'
                description_str += '\n**I respirator**: ' +\
                                    f'{locale.format_string("%d", respiratory, grouping=True)}'

                if tilstand == 'confirmed':
                    data = get('https://redutv-api.vg.no/corona/v1/sheets/fhi/gender').json()
                    male = f'{data["current"]["male"]}%'.replace('.', ',')
                    female = f'{data["current"]["female"]}%'.replace('.', ',')
                    description_str += f'\n\n**Menn**: {male}\n**Kvinner**: {female}'
            except:
                return await Defaults.error_fatal_send(ctx, text='Kunne ikke hente data')

            embed = discord.Embed(color=0xFF9C00, title='Koronaviruset - Norge', description=description_str)
            embed.set_author(name='VG', icon_url='https://pbs.twimg.com/profile_images/3077886704' +
                                                 '/4be85226137dc5e1eadbaa5526fe5f9e.jpeg')
            await Defaults.set_footer(ctx, embed)
            await ctx.send(embed=embed)

    @commands.cooldown(1, 5, commands.BucketType.guild)
    @corona.command(aliases=['municipality'])
    async def kommune(self, ctx, *, kommune: str):
        """Viser antall smittede/døde i en kommune"""

        async with ctx.channel.typing():

            try:
                url = 'https://redutv-api.vg.no/corona/v1/sheets/norway-table-overview/?region=municipality'
                data = get(url).json()
                municipality_name = None

                # Too lazy to do it any other way rn
                timestamp = data['updated']['ts'].replace('T', '')[:-6]
                timestamp = datetime.strptime(timestamp, '%Y-%m-%d%H:%M:%S')
                timestamp = timestamp.strftime('%H:%M %d.%m.%Y')

                for municipality in data['cases']:
                    if municipality['name'] is None:
                        continue
                    if municipality['name'].lower() == kommune.lower():
                        municipality_name = f'{municipality["name"]}, {municipality["parent"]}'
                        infected = municipality['confirmed']
                        dead = municipality['dead']
                        infected_per_capita = municipality['confirmedPer1kCapita']
                        break
                if municipality_name is None:
                    return await Defaults.error_warning_send(ctx, text='Enten eksisterer ikke kommunen, eller ' +
                                                                       'så er det ingen smittede/døde der')
            except:
                return await Defaults.error_fatal_send(ctx, text='Kunne ikke hente data')

            infected = locale.format_string('%d', infected, grouping=True)
            dead = locale.format_string('%d', dead, grouping=True)
            infected_per_capita = str(round(infected_per_capita, 2)).replace('.', ',')

            embed = discord.Embed(color=0xFF9C00, title=f'Koronaviruset - {municipality_name}')
            embed.description = '*Dataene er hentet fra ' +\
                                '[VG](https://www.vg.no/spesial/2020/corona-viruset/)*\n' +\
                                f'Sist oppdatert: {timestamp}'
            embed.set_author(name='VG', icon_url='https://pbs.twimg.com/profile_images/3077886704' +
                                                 '/4be85226137dc5e1eadbaa5526fe5f9e.jpeg')
            embed.add_field(name='Smittede', value=infected)
            embed.add_field(name='Døde', value=dead)
            embed.add_field(name='Smittede per tusen', value=infected_per_capita)
            await Defaults.set_footer(ctx, embed)
            await ctx.send(embed=embed)

    @commands.cooldown(1, 5, commands.BucketType.guild)
    @corona.command(aliases=['aldersfordeling', 'age'])
    async def alder(self, ctx):
        """Viser aldersfordelingen blant de smittede"""

        async with ctx.channel.typing():

            try:
                url = 'https://redutv-api.vg.no/corona/v1/sheets/fhi/age'
                data = get(url).json()

                timestamp = data['current']['date']
                timestamp = datetime.strptime(timestamp, '%Y-%m-%d').strftime('%d.%m.%Y')

                description_str = '***Smittede** i Norge fordelt på alder.\n' +\
                                    'Dataene er hentet fra ' +\
                                    '[VG](https://www.vg.no/spesial/2020/corona-viruset/)*\n' +\
                                    f'Sist oppdatert: {timestamp}\n\n'
                for agegroup, infected in data['current']['bins'].items():
                    description_str += f'**{agegroup} år**: {infected}\n'
            except:
                return await Defaults.error_fatal_send(ctx, text='Kunne ikke hente data')

            embed = discord.Embed(color=0xFF9C00, title='Koronaviruset - Aldersgrupper, Norge',
                                  description=description_str)
            embed.set_author(name='VG', icon_url='https://pbs.twimg.com/profile_images/3077886704' +
                                                 '/4be85226137dc5e1eadbaa5526fe5f9e.jpeg')
            await Defaults.set_footer(ctx, embed)
            await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Corona(bot))
