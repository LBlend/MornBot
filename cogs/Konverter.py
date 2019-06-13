import discord
from discord.ext import commands

from codecs import open
from json import load as json_load

from requests import get
from datetime import datetime
from re import sub

from cogs.utils import Defaults

with open('config.json', 'r', encoding='utf8') as f:
    config = json_load(f)
    prefix = config['prefix']
    ksoft_auth = config['ksoft_authentication']


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
            return await Defaults.error_warning_send(
                ctx,
                text='Det du har skrevet inn er ikke et tall\n\n' +
                     f'Skriv `{prefix}help {ctx.command}` for hjelp',
                mention=False)

        if tall > 1000000000 or tall < -1000000000:
            return await Defaults.error_warning_send(
                ctx, text='Tallet du har skrevet er for lavt/høyt!',
                mention=False)

        temp_celcius = round((float(tall) - 32) / 9 * 5, 2)

        embed = discord.Embed(
            color=ctx.me.color,
            description=f'`{tall} °F` :arrow_right: `{temp_celcius} °C`')
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
            return await Defaults.error_warning_send(
                ctx,
                text='Det du har skrevet inn er ikke et tall\n\n' +
                     f'Skriv `{prefix}help {ctx.command}` for hjelp',
                mention=False)

        if tall > 1000000000 or tall < -1000000000:
            return await Defaults.error_warning_send(
                ctx, text='Tallet du har skrevet er for lavt/høyt!',
                mention=False)

        temp_fahrenheit = round((float(tall) * 9) / 5 + 32, 2)

        embed = discord.Embed(
            color=ctx.me.color,
            description=f'`{tall} °C` :arrow_right: `{temp_fahrenheit} °F`')
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
            return await Defaults.error_warning_send(
                ctx,
                text='Det du har skrevet inn er ikke et tall\n\n' +
                     f'Skriv `{prefix}help {ctx.command}` for hjelp',
                mention=False)

        if vekt_kg > 1000000000 or vekt_kg < -1000000000:
            return await Defaults.error_warning_send(
                ctx, text='Tallet du har skrevet er for lavt/høyt!',
                mention=False)

        if høyde_meter > 1000000000 or høyde_meter < -1000000000:
            return await Defaults.error_warning_send(
                ctx, text='Tallet du har skrevet er for lavt/høyt!',
                mention=False)

        bmi = round(vekt_kg / (høyde_meter * høyde_meter), 2)

        embed = discord.Embed(color=ctx.me.color)
        if bmi < 18.5:
            text = 'Dette vil si at du er undervektig. ' +\
                   'Gå og nyt en burger du :)'
        elif bmi > 25:
            text = 'Dette vil si at du er overvektig. ' +\
                   'Få ræva i gir istedenfor å sitte på Discord!'
        else:
            text = 'Dette er en sunn BMI. Bra Jobba!'

        embed.add_field(name='BMI', value=f'`{bmi}`\n{text}')
        await ctx.send(embed=embed)

    @commands.bot_has_permissions(embed_links=True)
    @commands.cooldown(1, 5, commands.BucketType.guild)
    @commands.command(aliases=['penger', 'money', 'currency'])
    async def valuta(self, ctx, til_valuta, verdi, fra_valuta):
        """Se hvor mye noe er verdt i en annen valuta"""

        embed = discord.Embed(description='Laster...')
        status_msg = await ctx.send(embed=embed)

        if ',' in verdi:
            verdi = sub(',', '.', verdi)

        try:
            verdi = float(verdi)
        except ValueError:
            return await Defaults.error_warning_edit(
                ctx, status_msg,
                text='Sjekk om du har skrevet riktig tall\n\n' +
                     f'Skriv `{prefix}help {ctx.command}` for hjelp',
                mention=False)

        if verdi > 1000000000 or verdi < -1000000000:
            return await Defaults.error_warning_edit(
                ctx, status_msg,
                text='Tallet du har skrevet er for lavt/høyt!',
                mention=False)

        try:
            data = get(
                'https://api.ksoft.si/kumo/currency',
                headers={'Authorization': 'Bearer ' + ksoft_auth},
                params={
                    'from': fra_valuta,
                    'to': til_valuta,
                    'value': verdi}).json()
            value = data['pretty']

            embed = discord.Embed(
                color=ctx.me.color,
                description=f'`{verdi} {fra_valuta.upper()}` ' +
                f':arrow_right: `{value}`',
                timestamp=datetime.utcnow())
            await status_msg.edit(embed=embed)

        except KeyError:
            return await Defaults.error_warning_edit(
                ctx, status_msg,
                text='Sjekk om du har satt gyldige valutaer\n\n' +
                     f'Skriv `{prefix}help {ctx.command}` for hjelp',
                mention=False)

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
            return await Defaults.error_warning_send(
                ctx,
                text='Du må gi meg et tall\n\n' +
                     f'Skriv `{prefix}help {ctx.command}` for hjelp',
                mention=False
            )

        if tall > 1000000000 or tall < -1000000000:
            return await Defaults.error_warning_send(
                ctx, text='Tallet du har skrevet er for lavt/høyt',
                mention=False)

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
        except:
            return await Defaults.error_warning_send(
                ctx, text='Ugyldig måleenhet. Prøv en av følgende ```\n' +
                          'mm\ncm\nm\nkm\n```', mention=False)

        size_km = tall / måleenhet
        bananas = round(size_km / 0.0001778, 2)

        embed = discord.Embed(
            color=ctx.me.color,
            description=f'`{tall}{meassurement_type}` ' +
                        f':arrow_right: `{bananas} 🍌`')
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Konverter(bot))
