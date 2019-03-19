import discord
import asyncio
from discord.ext import commands

import codecs
import json
import random
import urllib.parse
import requests
from datetime import datetime

with codecs.open("config.json", "r", encoding="utf8") as f:
    config = json.load(f)
    prefix = config["prefix"]
    ksoftAuthentication = config["ksoftAuthentication"]

class Konverter:
    def __init__(self, bot):
        self.bot = bot


    @commands.cooldown(1, 2, commands.BucketType.guild)
    @commands.command(aliases=["fahrenheittocelcius"])
    async def ftc(self, ctx, tall):
        """Konverterer temperatur fra fahrenheit til celcius"""

         #   Sjekk riktig bruk av desimaltegn
        if "," in tall:
            embed = discord.Embed(color=0xFF0000, description=":x: Du må bruke `.` istedenfor `,`")
            await ctx.send(embed=embed)
            return

        try:
            tempCelcius = round((float(tall) - 32) / 9 * 5, 2)
        except:
            embed = discord.Embed(color=0xFF0000, description=f":x: Noe gikk galt\n\nSkriv `{prefix}help ftc` for hjelp")
            await ctx.send(embed=embed)
            return
        
        embed = discord.Embed(color=0x0085ff, description=f"`{tall} °F` :arrow_right: `{tempCelcius} °C`")
        await ctx.send(embed=embed)
    

    @commands.cooldown(1, 2, commands.BucketType.guild)
    @commands.command(aliases=["celciustofahrenheit"])
    async def ctf(self, ctx, tall):
        """Konverterer temperatur fra celcius til fahrenheit"""

        if "," in tall:
            embed = discord.Embed(color=0xFF0000, description=":x: Du må bruke `.` istedenfor `,`")
            await ctx.send(embed=embed)
            return

        #   Regn ut
        try:
            tempFahrenheit = round((float(tall) * 9) / 5 + 32, 2)
        except:
            embed = discord.Embed(color=0xFF0000, description=f":x: Noe gikk galt\n\nSkriv `{prefix}help ctf` for hjelp")
            await ctx.send(embed=embed)
            return
        
        embed = discord.Embed(color=0x0085ff, description=f"`{tall} °C` :arrow_right: `{tempFahrenheit} °F`")
        await ctx.send(embed=embed)
        

    @commands.cooldown(1, 2, commands.BucketType.guild)
    @commands.command()
    async def bmi(self, ctx, vekt_kg, høyde_meter):
        """Beregner BMIen din"""

        #   Sjekk riktig bruk av desimaltegn
        if "," in vekt_kg or "," in høyde_meter:
            embed = discord.Embed(color=0xFF0000, description=":x: Du må bruke `.` istedenfor `,`")
            await ctx.send(embed=embed)
            return

        #   Regn ut
        try:
            calculatedBMI = round(float(vekt_kg) / float(float(høyde_meter) * float(høyde_meter)), 2)
        except:
            embed = discord.Embed(color=0xFF0000, description=f":x: Noe gikk galt\n\nSkriv `{prefix}help bmi` for hjelp")
            await ctx.send(embed=embed)
            return

        embed = discord.Embed(color=0x0085ff)
        if calculatedBMI < 18.5:
            txt = "Dette vil si at du er undervektig. Gå og nyt en burger du :)"
        elif calculatedBMI > 25:
            txt = "Dette vil si at du er overvektig. Få ræva i gir istedenfor å sitte på Discord!"
        else:
            txt = "Dette er en sunn BMI. Bra Jobba!"
        
        embed.add_field(name="BMI", value=f"`{calculatedBMI}`\n{txt}")
        await ctx.send(embed=embed)


    @commands.cooldown(1, 5, commands.BucketType.guild)
    @commands.command(aliases=["penger", "money", "currency"])
    async def valuta(self, ctx, til_valuta, verdi, fra_valuta):
        """Se hvor mye noe er verdt i en annen valuta"""

        embed = discord.Embed(description="Laster...")
        statusmsg = await ctx.send(embed=embed)

        #   Sjekk riktig bruk av desimaltegn
        if "," in verdi:
            embed = discord.Embed(color=0xFF0000, description=":x: Du må bruke `.` istedenfor `,`")
            await ctx.send(embed=embed)
            return
        
        try:
            data = requests.get("https://api.ksoft.si/kumo/currency", headers={"Authorization":"Bearer " + ksoftAuthentication}, params={"from": fra_valuta, "to": til_valuta, "value": float(verdi)}).json()
            value = data["pretty"]

            embed = discord.Embed(color=0x0085ff, description=f"`{verdi} {fra_valuta.upper()}` :arrow_right: `{value}`", timestamp=datetime.utcnow())
            await statusmsg.edit(embed=embed)

        except:
            embed = discord.Embed(color=0xFF0000, description=f":x: Noe gikk galt\n\nSkriv `{prefix}help valuta` for hjelp")
            await statusmsg.edit(embed=embed)
            return


def setup(bot):
    bot.add_cog(Konverter(bot))