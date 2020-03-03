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
    @commands.cooldown(1, 5, commands.BucketType.guild)
    @commands.command(aliases=['coronavirus'])
    async def corona(self, ctx):
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
                        norway_updated = datetime.utcfromtimestamp(i['Last_Update'] / 1000).strftime('%d.%m.%Y %H:%M')
                        break
            except:
                return await Defaults.error_fatal_send(ctx, text='Kunne ikke hente data')

            embed = discord.Embed(color=0xFF9C00, title='Corona-viruset', url='https://github.com/CSSEGISandData/COVID-19')
            embed.description = f'Sist oppdatert (Norsk statistikk): {norway_updated} UTC'
            embed.add_field(name='Smittede', value=infected)
            embed.add_field(name='Døde', value=dead)
            embed.add_field(name='Friskmeldte', value=recovered)
            embed.add_field(name='Smittede i Norge', value=norway_infected)
            embed.add_field(name='Døde i Norge', value=norway_dead)
            embed.add_field(name='Friskmeldte i Norge', value=norway_recovered)
            await Defaults.set_footer(ctx, embed)
            await ctx.send(embed=embed)



def setup(bot):
    bot.add_cog(Corona(bot))