import discord
import asyncio
from discord.ext import commands

import codecs
import json
import requests
import random

class Misc:
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def smug(self, ctx):
        """Sender et smug bilde"""

        #   Hent data
        apiUrl = "https://nekos.life/api/v2/img/smug"
        data = requests.get(apiUrl).json()
        smug = data["url"]

        #   Embed
        embed = discord.Embed(color=0x0085ff)
        embed.description = "Smug"
        embed.set_image(url=smug)
        await ctx.send(embed=embed)     

    @commands.command(aliases=["voff", "doggo", "dog", "hund", "bikkje"])
    async def woof(self, ctx):
        """Sender en tilfeldig bissevoff"""

        #   Hent data
        apiUrl = "https://nekos.life/api/v2/img/woof"
        woofData = requests.get(apiUrl).json()
        woof = woofData["url"]

        #   Embed
        embed = discord.Embed(color=0x0085ff)
        embed.description = "Voff"
        embed.set_image(url=woof)
        await ctx.send(embed=embed)

    @commands.command(aliases=["kukstørrelse", "pikkstørrelse"])
    async def dicksize(self, ctx):
        """Se hvor liten pikk du har"""

        #   Last inn brukerdata
        with codecs.open(f"./assets/userdata/{ctx.message.author.id}.json", "r", encoding="utf8") as f:
            userdata = json.load(f)
            
            #   Sjekk om bruker har blitt gitt dicksize
            if userdata["dickSize"] == None:
                randomnumber = random.randint(0, 20)
                userdata["dickSize"] = randomnumber
                with codecs.open(f"./assets/userdata/{ctx.message.author.id}.json", "w", encoding="utf8") as f:
                    f.write(json.dumps(userdata))
                    
            #   Send Melding
            dicksize = userdata["dickSize"]
            await ctx.send(f"{dicksize} cm")

    @commands.command()
    async def roll(self, ctx, *args):
        """Gir deg et tilfeldig tall\n\nEksmpel: m!roll IQ-en min"""

        await ctx.send(str(random.randint(0, 100)))

    @commands.command(name="8ball")
    async def ball8(self, ctx, *args):
        """Svarer på dine dypeste spørsmål\n\nEksmpel: m!8ball er jeg dritt til å lage båtts?"""

        answers = ['Det er sannsynlig', 'Uten tvil', 'Ja', 'Man kan vel si det ja', 'Ehm, tror det er best vi ikke snakker om det jeg :sweat_smile:', 'нет', 'Nei ass', 'Er ikke så sannsynlig', 'I følge mine beregninger... nei']
        await ctx.send(random.choice(answers))

    @commands.command(aliases=["owoify", "uwu"])
    async def owo(self, ctx, *args):
        """Oversetter teksten din til owo\n\nEksmpel: m!owo jeg elsker pikk!"""

        #   Hent data
        try:
            owoApi = f"https://nekos.life/api/v2/owoify?text={args}"
            data = requests.get(owoApi).json()
            owoRaw = str(data["owo"][2:-2])
            owo = owoRaw.replace("', '", " ")
            await ctx.send(owo)
        
        #   Error
        except:
            await ctx.send("oopsie whoopsie you made a fucky wucky, no text or text over 200")
    
    @commands.command(aliases=["urban", "meaning", "mening", "betydning", "dictionary", "ordbok"])
    async def urbandictionary(self, ctx, *ord):
        """Sjekk definisjonen av et ord\n\nEksmpel: m!urban loli"""

        #   Hent data
        try:
            dataUrl = f"https://api.urbandictionary.com/v0/define?term={ord}"
            data = requests.get(urbanApi).json()

            randomDefinition = random.randint(0, 8)

            definitionUrl = data["list"][randomDefinition]["permalink"]
            word = data["list"][randomDefinition]["word"]
            submitter = data["list"][randomDefinition]["author"]

            de = data["list"][randomDefinition]["definition"]
            definition = de.replace("[", "").replace("]", "").replace(";", "")
            ex = data["list"][randomDefinition]["example"]
            example = ex.replace("[", "").replace("]", "").replace(";", "")

            thumbsUp = data["list"][randomDefinition]["thumbs_up"]
            thumbsDown = data["list"][randomDefinition]["thumbs_down"]
            
            #   Embed
            embed = discord.Embed(title=word, color=0x0085ff, url=definitionUrl, description= f"**Definert av:** {submitter}")
            embed.set_author(name="Urban Dictionary", icon_url="https://a2.mzstatic.com/us/r30/Purple/v4/dd/ef/75/ddef75c7-d26c-ce82-4e3c-9b07ff0871a5/mzl.yvlduoxl.png")
            embed.set_footer(text=f"{ctx.message.author.name}#{ctx.message.author.discriminator}", icon_url=ctx.message.author.avatar_url)
            embed.add_field(name="Definisjon", value=definition)
            embed.add_field(name="Eksempel", value=example)
            embed.add_field(name="Vurdering", value=f":thumbsup: {thumbsUp} / :thumbsdown: {thumbsDown}", inline=False)
            await ctx.send(embed=embed)

        #   Error
        except:
            await ctx.send("Prøv igjen. Prøv kanskje et annet ord?")
        

def setup(bot):
    bot.add_cog(Misc(bot))