import discord
import asyncio
from discord.ext import commands

import codecs
import json
import requests
import random
from hashlib import md5

with codecs.open("config.json", "r", encoding="utf8") as f:
    config = json.load(f)
    prefix = config["prefix"]

class Misc:
    def __init__(self, bot):
        self.bot = bot


    @commands.cooldown(1, 5, commands.BucketType.guild)
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


    @commands.cooldown(1, 5, commands.BucketType.guild)
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


    @commands.cooldown(1, 2, commands.BucketType.guild)
    @commands.command(aliases=["kukstørrelse", "pikkstørrelse"])
    async def dicksize(self, ctx, bruker: discord.Member=None):
        """Se hvor liten pikk du har"""
        
        #   Om ingen bruker gitt, sett bruker til author
        if not bruker:
            bruker = ctx.message.author
        
        userid = bruker.id

        def hashDicksize(userid, upper, lower):
            dickhash = md5(str(userid).encode("utf-8")).hexdigest()
            return int(int(dickhash[11:13], 16)*(upper-lower)/255 + lower)

        #   Må jo gi meg selv en stor kuk
        if bruker.id == 170506717140877312:
            dicksize = 69
        else:
            dicksize = hashDicksize(userid, 25, 2)

        #   Tegning
        dickDrawing = "=" * dicksize

        embed = discord.Embed(color=0x0085ff)
        embed.set_author(name=f"{bruker.name}#{bruker.discriminator}", icon_url=bruker.avatar_url)
        embed.add_field(name="Kukstørrelse", value=f"{dicksize} cm\n8{dickDrawing}D")
        await ctx.send(embed=embed)


    @commands.cooldown(1, 2, commands.BucketType.guild)
    @commands.command()
    async def roll(self, ctx, *args):
        """Gir deg et tilfeldig talln"""

        await ctx.send(str(random.randint(0, 100)))


    @commands.cooldown(1, 2, commands.BucketType.guild)
    @commands.command(name="8ball")
    async def ball8(self, ctx, *args):
        """Svarer på dine dypeste spørsmål"""

        answers = ["Det er sannsynlig", "Uten tvil", "Ja", "Man kan vel si det ja", "Ehm, tror det er best vi ikke snakker om det jeg :sweat_smile:", "нет", "Nei ass", "Er ikke så sannsynlig", "I følge mine beregninger... nei"]
        await ctx.send(random.choice(answers))


    @commands.cooldown(1, 2, commands.BucketType.guild)
    @commands.command(aliases=["reverse"])
    async def reverser(self, ctx, *, tekst):
        """Reverserer tekst"""

        await ctx.send(tekst[::-1])


    @commands.cooldown(1, 5, commands.BucketType.guild)
    @commands.command(aliases=["owoify", "uwu"])
    async def owo(self, ctx, *setning):
        """Oversetter teksten din til owo"""

        #   Sjekk for error & Hent data
        try:
            owoApi = f"https://nekos.life/api/v2/owoify?text={setning}"
            data = requests.get(owoApi).json()

            owoRaw = str(data["owo"][2:-2])
            owo = owoRaw.replace(",", "").replace("'", "")
            await ctx.send(owo)

        except:
            await ctx.send("oopsie whoopsie you made a fucky wucky, no text or text over 200")
    

    @commands.cooldown(1, 5, commands.BucketType.guild)
    @commands.command(aliases=["urban", "meaning", "mening", "betydning", "dictionary", "ordbok"])
    async def urbandictionary(self, ctx, *ord):
        """Sjekk definisjonen av et ord"""

        #   Sjekk for error
        try:
            dataUrl = f"https://api.urbandictionary.com/v0/define?term={ord}"
            data = requests.get(dataUrl).json()

            randomDefinition = random.randint(0, 8)

            definitionUrl = data["list"][randomDefinition]["permalink"]

        except:
            await ctx.send(f"Noe gikk galt\nPrøv kanskje et annet ord?\nSkriv `{prefix}help urban` for hjelp")
            return

        #   Hent restn av data
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
        

def setup(bot):
    bot.add_cog(Misc(bot))