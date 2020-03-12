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
    @commands.group(aliases=['korona', 'coronavirus', 'koronavirus'])
    async def corona(self, ctx):
        """Viser status på Koronaviruset"""

        if ctx.invoked_subcommand is None:
            await self.verden.invoke(ctx)

    @commands.cooldown(1, 5, commands.BucketType.guild)
    @corona.command(aliases=['global'])
    async def verden(self, ctx):
        """Viser antall døde/smittede/friskmeldte av corona-virsuet"""

        async with ctx.channel.typing():
            try:
                url = 'https://services1.arcgis.com/0MSEUqKaxRlEPj5g/arcgis/rest/services/ncov_cases/FeatureServer/1/query?f=json&where=1%3D1&returnGeometry=false&spatialRel=esriSpatialRelIntersects&outStatistics=%5B%7B%22statisticType%22%3A%22sum%22%2C%22onStatisticField%22%3A%22Confirmed%22%2C%22outStatisticFieldName%22%3A%22confirmed%22%7D%2C%20%7B%22statisticType%22%3A%22sum%22%2C%22onStatisticField%22%3A%22Deaths%22%2C%22outStatisticFieldName%22%3A%22deaths%22%7D%2C%20%7B%22statisticType%22%3A%22sum%22%2C%22onStatisticField%22%3A%22Recovered%22%2C%22outStatisticFieldName%22%3A%22recovered%22%7D%5D&outSR=102100&cacheHint=false'
                data = get(url).json()
                infected = locale.format_string('%d', data['features'][0]['attributes']['confirmed'], grouping=True)
                dead = locale.format_string('%d', data['features'][0]['attributes']['deaths'], grouping=True)
                recovered = locale.format_string('%d', data['features'][0]['attributes']['recovered'], grouping=True)

                url = 'https://services1.arcgis.com/0MSEUqKaxRlEPj5g/arcgis/rest/services/ncov_cases/FeatureServer/2/query?f=json&where=Confirmed%20%3E%200&returnGeometry=false&spatialRel=esriSpatialRelIntersects&outFields=*&orderByFields=Confirmed%20desc&resultOffset=0&resultRecordCount=100&cacheHint=false'
                data = get(url).json()
                for i in data['features']:
                    i = i['attributes']
                    if i['Country_Region'] == 'Norway':
                        norway_infected = locale.format_string('%d', i['Confirmed'], grouping=True)
                        norway_dead = locale.format_string('%d', i['Deaths'], grouping=True)
                        norway_recovered = locale.format_string('%d', i['Recovered'], grouping=True)
                        norway_updated = datetime.utcfromtimestamp(i['Last_Update'] / 1000).strftime('%H:%M - %d.%m.%Y')
                        break
            except:
                return await Defaults.error_fatal_send(ctx, text='Kunne ikke hente data')

            embed = discord.Embed(color=0xFF9C00, title='Koronaviruset')
            embed.description = f'Norsk statistikk sist oppdatert: {norway_updated} (UTC)'
            embed.add_field(name='Smittede', value=infected)
            embed.add_field(name='Døde', value=dead)
            embed.add_field(name='Friskmeldte', value=recovered)
            embed.add_field(name='Smittede i Norge', value=norway_infected)
            embed.add_field(name='Døde i Norge', value=norway_dead)
            embed.add_field(name='Friskmeldte i Norge', value=norway_recovered)
            await Defaults.set_footer(ctx, embed)
            await ctx.send(embed=embed)

    @commands.cooldown(1, 5, commands.BucketType.guild)
    @corona.command(aliases=['noreg', 'norway'])
    async def norge(self, ctx, *, tilstand: str=None):
        """Viser status i Norge fordelt på fylker"""

        conditions = {
            'smittede': 'confirmed',
            'døde': 'dead',
            'friskmeldte': 'recovered'
        }
        if tilstand is not None and tilstand.lower() in conditions:
            infected_str = f'*{tilstand.title()} i Norge fordelt på fylker.\n' +\
                            'Dataene oppdateres omtrent én gang om dagen.*\n\n'
            tilstand = conditions[tilstand]
        else:
            return await Defaults.error_warning_send(ctx, text='Du må velge en av følgende\n\n' +
            f'• `{self.bot.prefix}corona norge smittede`\n• `{self.bot.prefix}corona norge døde`\n' +
            f'• `{self.bot.prefix}corona norge friskmeldte`')

        async with ctx.channel.typing():

            try:
                url = 'https://www.vg.no/spesial/2020/corona-viruset/data/norway/'
                data = get(url).json()
                counties = []
                for i in data['cases']:
                    counties.append(data['cases'][i])

                def sortinfected(x):
                    return x['confirmed']
                def sortdead(x):
                    return x['dead']
                def sortrecovered(x):
                    return x['recovered']
                if tilstand == 'confirmed':
                    counties.sort(key=sortinfected)
                elif tilstand == 'dead':
                    counties.sort(key=sortdead)
                elif tilstand == 'recovered':
                    counties.sort(key=sortrecovered)
                counties.reverse()

                for i in counties:
                    infected_str += f'**{i["county"]}**: {locale.format_string("%d", i[tilstand], grouping=True)}\n'

                infected_str += f'\n\n**TOTALT**: {locale.format_string("%d", data["totals"][tilstand], grouping=True)}'
            except:
                return await Defaults.error_fatal_send(ctx, text='Kunne ikke hente data')

            embed = discord.Embed(color=0xFF9C00, title='Koronaviruset', description=infected_str)
            embed.set_author(name='VG', icon_url='https://pbs.twimg.com/profile_images/3077886704' +
                                                 '/4be85226137dc5e1eadbaa5526fe5f9e.jpeg')
            await Defaults.set_footer(ctx, embed)
            await ctx.send(embed=embed)

    @commands.cooldown(1, 5, commands.BucketType.guild)
    @corona.command(aliases=['municipality'])
    async def kommune(self, ctx, kommune: str):
        """Viser antall smittede/døde/friskmeldte i en kommune"""

        async with ctx.channel.typing():

            try:
                url = 'https://www.vg.no/spesial/2020/corona-viruset/data/norway/'
                data = get(url).json()
                municipality_name = None
                for county in data['cases']:
                    case = data['cases'][county]
                    for municipality in case['municipalities']:
                        if case['municipalities'][municipality]['kommunenavn'] is None:
                            continue
                        if case['municipalities'][municipality]['kommunenavn'].lower() == kommune.lower():
                            municipality_name = case['municipalities'][municipality]['kommunenavn']
                            infected = case['municipalities'][municipality]['confirmed']
                            dead = case['municipalities'][municipality]['dead']
                            recovered = case['municipalities'][municipality]['recovered']
                            break
                    if municipality_name is None:
                        return await Defaults.error_warning_send(ctx,
                        text='Enten så eksisterer ikke kommunen, eller så er det ingen smittede/døde/friskemldete der.')
            except:
                return await Defaults.error_fatal_send(ctx, text='Kunne ikke hente data')

            infected = locale.format_string('%d', infected, grouping=True)
            dead = locale.format_string('%d', dead, grouping=True)
            recovered = locale.format_string('%d', recovered, grouping=True)

            embed = discord.Embed(color=0xFF9C00, title=f'Koronaviruset - {municipality_name}')
            embed.description = '*Dataene oppdateres omtrent én gang om dagen.*'
            embed.set_author(name='VG', icon_url='https://pbs.twimg.com/profile_images/3077886704' +
                                                 '/4be85226137dc5e1eadbaa5526fe5f9e.jpeg')
            embed.add_field(name='Smittede', value=infected)
            embed.add_field(name='Døde', value=dead)
            embed.add_field(name='Friskmeldte', value=recovered)
            await Defaults.set_footer(ctx, embed)
            await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Corona(bot))
