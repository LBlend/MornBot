from discord.ext import commands
import discord

from requests import get
from datetime import datetime

from cogs.utils import Defaults


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
                url = 'https://services1.arcgis.com/0MSEUqKaxRlEPj5g/arcgis/rest/services/ncov_cases/FeatureServer/1/query?f=json&outStatistics=%5B%7B%22statisticType%22%3A%22sum%22%2C%22onStatisticField%22%3A%22Confirmed%22%2C%22outStatisticFieldName%22%3A%22confirmed%22%7D%2C%20%7B%22statisticType%22%3A%22sum%22%2C%22onStatisticField%22%3A%22Deaths%22%2C%22outStatisticFieldName%22%3A%22deaths%22%7D%2C%20%7B%22statisticType%22%3A%22sum%22%2C%22onStatisticField%22%3A%22Recovered%22%2C%22outStatisticFieldName%22%3A%22recovered%22%7D%5D'
                data = get(url).json()
                infected = data['features'][0]['attributes']['confirmed']
                dead = data['features'][0]['attributes']['deaths']
                recovered = data['features'][0]['attributes']['recovered']
            except KeyError:
                return await Defaults.error_fatal_send(ctx, text='Kunne ikke hente data')

            embed = discord.Embed(color=0xFF9C00, title='Corona-viruset')
            embed.description = datetime.now().strftime('%d.%m.%Y %H:%M')
            embed.add_field(name='Smittede', value=infected)
            embed.add_field(name='Døde', value=dead)
            embed.add_field(name='Friskmeldte', value=recovered)
            await Defaults.set_footer(ctx, embed)
            await ctx.send(embed=embed)



def setup(bot):
    bot.add_cog(Corona(bot))