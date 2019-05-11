import discord
from discord.ext import commands

from codecs import open
from json import load as json_load

from requests import get
from datetime import datetime
from re import sub

from .utils import Defaults

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
            temp_celcius = round((float(tall) - 32) / 9 * 5, 2)
        except ValueError:
            return await Defaults.error_warning_send(
                ctx,
                text='Det du har skrevet inn er ikke et tall\n\n' +
                     f'Skriv `{prefix}help {ctx.command}` for hjelp',
                mention=False)

        if temp_celcius > 1000000000000 or temp_celcius < -1000000000000:
            return await Defaults.error_warning_send(
                ctx, text='Tallet du har skrevet er for lavt/høyt!',
                mention=False)

        embed = discord.Embed(
            color=0x0085ff,
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
            temp_fahrenheit = round((float(tall) * 9) / 5 + 32, 2)
        except ValueError:
            return await Defaults.error_warning_send(
                ctx,
                text='Det du har skrevet inn er ikke et tall\n\n' +
                     f'Skriv `{prefix}help {ctx.command}` for hjelp',
                mention=False)

        if temp_fahrenheit > 1000000000000 or temp_fahrenheit < -1000000000000:
            return await Defaults.error_warning_send(
                ctx, text='Tallet du har skrevet er for lavt/høyt!',
                mention=False)

        embed = discord.Embed(
            color=0x0085ff,
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
            bmi = round(vekt_kg / (høyde_meter * høyde_meter), 2)
        except ValueError:
            return await Defaults.error_warning_send(
                ctx,
                text='Det du har skrevet inn er ikke et tall\n\n' +
                     f'Skriv `{prefix}help {ctx.command}` for hjelp',
                mention=False)

        if bmi > 50 or bmi <= 5:
            return await Defaults.error_warning_send(
                ctx,
                text='Sjekk om du har skrevet riktige tall. ' +
                     'Beregningen har gitt et usannsynlig svar\n\n' +
                     f'Skriv `{prefix}help {ctx.command}` for hjelp',
                mention=False)

        embed = discord.Embed(color=0x0085ff)
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
            return await Defaults.error_warning_send(
                ctx,
                text='Sjekk om du har skrevet riktige tall. ' +
                     'Beregningen har gitt et usannsynlig svar\n\n' +
                     f'Skriv `{prefix}help {ctx.command}` for hjelp',
                mention=False)

        if verdi > 1000000000000 or verdi < -1000000000000:
            return await Defaults.error_warning_send(
                ctx, text='Tallet du har skrevet er for lavt/høyt!',
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
                color=0x0085ff,
                description=f'`{verdi} {fra_valuta.upper()}` ' +
                f':arrow_right: `{value}`',
                timestamp=datetime.utcnow())
            await status_msg.edit(embed=embed)

        except KeyError:
            return await Defaults.error_warning_send(
                ctx,
                text='Sjekk om du har satt gyldige valutaer\n\n' +
                     f'Skriv `{prefix}help {ctx.command}` for hjelp',
                mention=False)


def setup(bot):
    bot.add_cog(Konverter(bot))
