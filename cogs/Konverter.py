from discord.ext import commands
import discord

import locale

from requests import get
from datetime import datetime
from re import sub

from cogs.utils import Defaults


locale.setlocale(locale.LC_ALL, '')


class Konverter(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.bot_has_permissions(embed_links=True)
    @commands.cooldown(1, 2, commands.BucketType.guild)
    @commands.command(aliases=['fahrenheittocelcius'])
    async def ftc(self, ctx, tall):
        """Konverterer temperatur fra fahrenheit til celcius"""

        if ',' in tall:
            tall = sub(',', '.', tall)

        try:
            tall = float(tall)
        except ValueError:
            return await Defaults.error_warning_send(ctx, text='Det du har skrevet inn er ikke et tall\n\n' +
                                                               f'Skriv `{self.bot.prefix}help {ctx.command}` for hjelp')

        if tall > 1000000000 or tall < -1000000000:
            return await Defaults.error_warning_send(ctx, text='Tallet du har skrevet er for lavt/høyt!')

        temp_celcius = (tall - 32) / 9 * 5

        tall = locale.format_string('%.2f', tall, grouping=True)
        temp_celcius = locale.format_string('%.2f', temp_celcius, grouping=True)

        embed = discord.Embed(color=ctx.me.color, description=f'`{tall} °F` ➡️ `{temp_celcius} °C`')
        await Defaults.set_footer(ctx, embed)
        await ctx.send(embed=embed)

    @commands.bot_has_permissions(embed_links=True)
    @commands.cooldown(1, 2, commands.BucketType.guild)
    @commands.command(aliases=['celciustofahrenheit'])
    async def ctf(self, ctx, tall):
        """Konverterer temperatur fra celcius til fahrenheit"""

        if ',' in tall:
            tall = sub(',', '.', tall)

        try:
            tall = float(tall)
        except ValueError:
            return await Defaults.error_warning_send(ctx, text='Det du har skrevet inn er ikke et tall\n\n' +
                                                               f'Skriv `{self.bot.prefix}help {ctx.command}` for hjelp')

        if tall > 1000000000 or tall < -1000000000:
            return await Defaults.error_warning_send(ctx, text='Tallet du har skrevet er for lavt/høyt!')

        temp_fahrenheit = (tall * 9) / 5 + 32

        tall = locale.format_string('%.2f', tall, grouping=True)
        temp_fahrenheit = locale.format_string('%.2f', temp_fahrenheit, grouping=True)

        embed = discord.Embed(color=ctx.me.color, description=f'`{tall} °C` ➡️ `{temp_fahrenheit} °F`')
        await Defaults.set_footer(ctx, embed)
        await ctx.send(embed=embed)

    @commands.bot_has_permissions(embed_links=True)
    @commands.cooldown(1, 2, commands.BucketType.guild)
    @commands.command()
    async def bmi(self, ctx, vekt_kg, høyde_meter):
        """Beregner BMIen din"""

        if ',' in vekt_kg or ',' in høyde_meter:
            vekt_kg = sub(',', '.', vekt_kg)
            høyde_meter = sub(',', '.', høyde_meter)

        try:
            vekt_kg = float(vekt_kg)
            høyde_meter = float(høyde_meter)
        except ValueError:
            return await Defaults.error_warning_send(ctx, text='Det du har skrevet inn er ikke et tall\n\n'
                                                               f'Skriv `{self.bot.prefix}help {ctx.command}` for hjelp')

        if vekt_kg > 1000000000 or vekt_kg < 0:
            return await Defaults.error_warning_send(ctx, text='Tallet du har skrevet er for lavt/høyt!')

        if høyde_meter > 1000000000 or høyde_meter < 0:
            return await Defaults.error_warning_send(ctx, text='Tallet du har skrevet er for lavt/høyt!')

        bmi = round(vekt_kg / (høyde_meter * høyde_meter))

        embed = discord.Embed(color=ctx.me.color)
        if bmi < 18.5:
            text = 'Dette vil si at du er undervektig. Gå og nyt en burger du :)'
        elif bmi > 25:
            text = 'Dette vil si at du er overvektig. Få ræva i gir istedenfor å sitte på Discord!'
        else:
            text = 'Dette er en sunn BMI. Bra Jobba!'

        embed.add_field(name='BMI', value=f'`{bmi}`\n{text}')
        await Defaults.set_footer(ctx, embed)
        await ctx.send(embed=embed)

    @commands.bot_has_permissions(embed_links=True)
    @commands.cooldown(1, 5, commands.BucketType.guild)
    @commands.command(aliases=['penger', 'money', 'currency'])
    async def valuta(self, ctx, til_valuta: str, verdi, fra_valuta: str):
        """Se hvor mye noe er verdt i en annen valuta"""

        if ',' in verdi:
                verdi = sub(',', '.', verdi)

        try:
            verdi = float(verdi)
        except ValueError:
            return await Defaults.error_warning_send(ctx, text='Sjekk om du har skrevet riktig tall\n\n' +
                                                        f'Skriv `{self.bot.prefix}help {ctx.command}` for hjelp')

        if verdi > 1000000000 or verdi < 0:
            return await Defaults.error_warning_send(ctx, text='Tallet du har skrevet er for lavt/høyt!')

        fra_valuta = fra_valuta.upper()
        til_valuta = til_valuta.upper()

        currencies = ['AED', 'ARS', 'AUD', 'BGN', 'BRL', 'BSD', 'CAD', 'CHF', 'CLP', 'CNY', 'COP', 'CZK',
        'DKK', 'DOP', 'EGP', 'EUR', 'FJD', 'GBP', 'GTQ', 'HKD', 'HRK', 'HUF', 'IDR', 'ILS', 'INR', 'ISK',
        'JPY', 'KRW', 'KZT', 'MXN', 'MYR', 'NOK', 'NZD', 'PAB', 'PEN', 'PHP', 'PKR', 'PLN', 'PYG', 'RON',
        'RUB', 'SAR', 'SEK', 'SGD', 'THB', 'TRY', 'TWD', 'UAH', 'USD', 'UYU', 'ZAR']
        if fra_valuta not in currencies:
            return await Defaults.error_fatal_send(ctx, text=f'`{fra_valuta}` er ikke en gyldig valuta')
        if til_valuta not in currencies:
            return await Defaults.error_fatal_send(ctx, text=f'`{til_valuta}` er ikke en gyldig valuta')

        async with ctx.channel.typing():

            try:
                data = get(f'https://api.exchangerate-api.com/v4/latest/{fra_valuta}').json()
            except:
                return await Defaults.error_warning_send(ctx, text='API-tilkobling feilet!')

            value = verdi * data['rates'][til_valuta]

            verdi = locale.format_string('%.2f', verdi, grouping=True)
            value = locale.format_string('%.2f', value, grouping=True)

            embed = discord.Embed(color=ctx.me.color,
                                  description=f'`{verdi} {fra_valuta}` ➡️ `{value} {til_valuta}`',
                                  timestamp=datetime.utcnow())
            await Defaults.set_footer(ctx, embed)
            await ctx.send(embed=embed)

    @commands.bot_has_permissions(embed_links=True)
    @commands.cooldown(1, 2, commands.BucketType.guild)
    @commands.command(aliases=['banan', 'bananas', 'bananaforscale'])
    async def bananer(self, ctx, tall, måleenhet: str):
        """Banana for scale"""

        if ',' in tall:
            tall = sub(',', '.', tall)

        try:
            tall = float(tall)
        except ValueError:
            return await Defaults.error_warning_send(ctx, text='Du må gi meg et tall\n\n' +
                                                               f'Skriv `{self.bot.prefix}help {ctx.command}` for hjelp')

        if tall > 1000000000 or tall < 0:
            return await Defaults.error_warning_send(ctx, text='Tallet du har skrevet er for lavt/høyt')

        meassurements = {
            'mm': 1000000,
            'millimeter': 1000000,
            'millimeters': 1000000,
            'cm': 100000,
            'centimeter': 100000,
            'centimeters': 100000,
            'm': 1000,
            'meter': 1000,
            'meters': 1000,
            'km': 1,
            'kilometer': 1,
            'kilometers': 1
        }
        meassurement_type = måleenhet
        try:
            måleenhet = meassurements[måleenhet]
        except KeyError:
            return await Defaults.error_warning_send(ctx, text='Ugyldig måleenhet. Prøv en av følgende ```\n' +
                                                               'mm\ncm\nm\nkm\n```')

        size_km = tall / måleenhet
        bananas = size_km / 0.0001778

        tall = locale.format_string('%.2f', tall, grouping=True)
        bananas = locale.format_string('%.2f', bananas, grouping=True)

        embed = discord.Embed(color=ctx.me.color, description=f'`{tall} {meassurement_type}` ➡️ `{bananas} 🍌`')
        await Defaults.set_footer(ctx, embed)
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Konverter(bot))
