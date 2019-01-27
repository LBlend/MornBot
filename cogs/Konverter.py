import discord
import asyncio
from discord.ext import commands

import codecs
import json
import random

with codecs.open("config.json", "r", encoding="utf8") as f:
    config = json.load(f)
    prefix = config["prefix"]

class Konverter:
    def __init__(self, bot):
        self.bot = bot


    @commands.cooldown(1, 2, commands.BucketType.guild)
    @commands.command(aliases=["fahrenheittocelcius"])
    async def ftc(self, ctx, tall):
        """Konverterer temperatur fra fahrenheit til celcius"""

         #   Sjekk riktig bruk av desimaltegn
        if "," in tall:
            await ctx.send("Du må bruke `.` istedenfor `,`")
            return

        try:
            tempCelcius = round((float(tall) - 32) / 9 * 5, 2)
        except:
            await ctx.send(f"Noe gikk galt\nSkriv `{prefix}help ftc` for hjelp")
            return
        
        await ctx.send(f"`{tall} °F` = `{tempCelcius} °C`")
    

    @commands.cooldown(1, 2, commands.BucketType.guild)
    @commands.command(aliases=["celciustofahrenheit"])
    async def ctf(self, ctx, tall):
        """Konverterer temperatur fra celcius til fahrenheit"""

        if "," in tall:
            await ctx.send("Du må bruke `.` istedenfor `,`")
            return

        #   Regn ut
        try:
            tempFahrenheit = round((float(tall) * 9) / 5 + 32, 2)
        except:
            await ctx.send(f"Noe gikk galt\nSkriv `{prefix}help ctf` for hjelp")
            return
            
        await ctx.send(f"`{tall} °C` = `{tempFahrenheit} °F`")
        

    @commands.cooldown(1, 2, commands.BucketType.guild)
    @commands.command()
    async def bmi(self, ctx, vekt_kg, høyde_meter):
        """Beregner BMIen din"""

        #   Sjekk riktig bruk av desimaltegn
        if "," in vekt_kg or "," in høyde_meter:
            await ctx.send("Du må bruke `.` istedenfor `,`")
            return

        #   Regn ut
        try:
            calculatedBMI = round(float(vekt_kg) / float(float(høyde_meter) * float(høyde_meter)), 2)
        except:
            await ctx.send(f"Noe gikk galt\nSkriv `{prefix}help bmi` for hjelp")
            return

        if calculatedBMI < 18.5:
            await ctx.send(f"Du har en BMI på `{calculatedBMI}`\nDette vil si at du er undervektig. Gå og nyt en burger du :)")
        elif calculatedBMI > 25:
            await ctx.send(f"Du har en BMI på `{calculatedBMI}`\nDette vil si at du er overvektig. Få ræva i gir istedenfor å sitte på Discord!")
        else:
            await ctx.send(f"Du har en BMI på `{calculatedBMI}`\nDette er en sunn BMI. Bra Jobba!")
        

def setup(bot):
    bot.add_cog(Konverter(bot))