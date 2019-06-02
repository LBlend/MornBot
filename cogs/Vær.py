import discord
from discord.ext import commands

from codecs import open
from json import load as json_load

from requests import get
import urllib.parse
from datetime import datetime

from .utils import Defaults

with open('config.json', 'r', encoding='utf8') as f:
    config = json_load(f)
    prefix = config['prefix']
    openweathermap_api_key = config['openweathermap_api_key']


class Vær(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.bot_has_permissions(embed_links=True)
    @commands.cooldown(1, 5, commands.BucketType.guild)
    @commands.command(aliases=['weather', 'forecast', 'værmelding', 'yr'])
    async def vær(self, ctx, *, by=None):
        """Viser været i en valgt by"""

        if not by:
            return await Defaults.error_warning_send(
                ctx, text='Du må gi meg en by\n\n' +
                          f'Skriv `{prefix}help {ctx.command}` for hjelp')

        async with ctx.channel.typing():

            try:
                url = 'http://api.openweathermap.org/data/2.5/weather?' + \
                      urllib.parse.urlencode({
                          'appid': openweathermap_api_key, 'q': by})
                data = get(url).json()
                city_id = str(data['id'])
            except KeyError:
                return await Defaults.error_fatal_send(
                    ctx, text='Kan ikke finne værdata for denne byen!',
                    mention=False)

            link = f'https://openweathermap.org/city/{city_id}'
            city_name = data['name']
            country_code = data['sys']['country'].lower()
            fetch_date = datetime.fromtimestamp(
                data['dt']).strftime('%d.%m.%Y %H:%M')
            description = data['weather'][0]['description']
            temp_celcius = round((data['main']['temp']) - 273)
            temp_fahrenheit = round(1.8 * ((data['main']['temp']) - 273) + 32)
            wind_speed = data['wind']['speed']
            humidity = data['main']['humidity']
            cloudiness = data['clouds']['all']
            sunrise = datetime.fromtimestamp(
                data['sys']['sunrise']).strftime('%H:%M')
            sunset = datetime.fromtimestamp(
                data['sys']['sunset']).strftime('%H:%M')
            time_now = datetime.now().strftime('%d.%m.%Y %H:%M')

            embed = discord.Embed(
                title=f':flag_{country_code}: {city_name}, ' +
                f'{country_code.upper()} | {fetch_date} (Norsk Tid)',
                color=ctx.me.color, url=link, description=description)
            embed.set_author(
                name='OpenWeatherMap',
                icon_url='https://pbs.twimg.com/profile_images/' +
                         '720298646630084608/wb7LSoAc_400x400.jpg')
            embed.add_field(
                name='Temperatur',
                value=f'{temp_celcius} °C\n{temp_fahrenheit} °F')
            embed.add_field(name='Vind', value=f'{wind_speed} m/s')
            embed.add_field(name='Luftfuktighet', value=f'{humidity}%')
            embed.add_field(name='Skyer', value=f'{cloudiness}%')
            embed.add_field(name='Soloppgang (Norsk tid)', value=sunrise)
            embed.add_field(name='Solnedgang (Norsk tid)', value=sunset)
            embed.set_footer(text=f'Tid i Norge nå: {time_now}')
            return await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Vær(bot))
