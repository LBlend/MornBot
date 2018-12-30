import discord
import asyncio
from discord.ext import commands

import random

class Konverter:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["fahrenheittocelcius"])
    async def ftc(self, ctx, tall):
        """Konverterer temperatur fra fahrenheit til celcius\n\nEksmpel: m!ftc 100"""

        try:
            tempCelcius = round((float(tall) - 32) / 9 * 5, 2)
            await ctx.send(f"`{tall} °F` = `{tempCelcius} °C`")
        except:
            await ctx.send("Noe gikk galt")
    
    @commands.command(aliases=["celciustofahrenheit"])
    async def ctf(self, ctx, tall):
        """Konverterer temperatur fra celcius til fahrenheit\n\nEksmpel: m!ctf 22"""

        #   Regn ut
        try:
            tempFahrenheit = round((float(tall) * 9) / 5 + 32, 2)
            await ctx.send(f"`{tall} °C` = `{tempFahrenheit} °F`")

        #   Error
        except:
            await ctx.send("Noe gikk galt")

    @commands.command()
    async def bmi(self, ctx, vekt_kg, høyde_meter):
        """Beregner BMIen din\n\nEksmpel: m!bmi 80 1.85"""

        #   Sjekk riktig bruk av desimaltegn
        if "," in vekt_kg or "," in høyde_meter:
            await ctx.send("Du må bruke `.` istedenfor `,`")
            return

        #   Regn ut
        calculatedBMI = round(float(vekt_kg) / float(float(høyde_meter) * float(høyde_meter)), 2)
        if calculatedBMI < 18.5:
            await ctx.send(f"Du har en BMI på `{calculatedBMI}`\nDette vil si at du er undervektig. Gå og nyt en burger du :)")
        elif calculatedBMI > 25:
            await ctx.send(f"Du har en BMI på `{calculatedBMI}`\nDette vil si at du er overvektig. Få ræva i gir istedenfor å sitte på Discord!")
        else:
            await ctx.send(f"Du har en BMI på `{calculatedBMI}`\nDette er en sunn BMI. Bra Jobba!")
        

def setup(bot):
    bot.add_cog(Konverter(bot))