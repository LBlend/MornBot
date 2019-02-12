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

        embed = discord.Embed(description="Laster...")
        statusmsg = await ctx.send(embed=embed)

        #   Hent data
        data = requests.get("https://nekos.life/api/v2/img/smug").json()
        smug = data["url"]

        #   Embed
        embed = discord.Embed(color=0x0085ff)
        embed.set_image(url=smug)
        await statusmsg.edit(embed=embed)     


    @commands.cooldown(1, 5, commands.BucketType.guild)
    @commands.command(aliases=["voff", "doggo", "dog", "hund", "bikkje"])
    async def woof(self, ctx):
        """Sender en tilfeldig bissevoff"""

        embed = discord.Embed(description="Laster...")
        statusmsg = await ctx.send(embed=embed)

        #   Hent data
        woofData = requests.get("https://nekos.life/api/v2/img/woof").json()
        woof = woofData["url"]

        #   Embed
        embed = discord.Embed(color=0x0085ff)
        embed.set_image(url=woof)
        await statusmsg.edit(embed=embed)


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
        """Gir deg et tilfeldig tall"""

        await ctx.send(str(random.randint(0, 100)))


    @commands.cooldown(1, 2, commands.BucketType.guild)
    @commands.command(name="8ball")
    async def ball8(self, ctx, *args):
        """Svarer på dine dypeste spørsmål"""

        if not "?" in ctx.message.content:
            await ctx.send("Du må stille meg et spørsmål da dømdøm!")
            return

        answers = ["Det er sannsynlig", "Uten tvil", "Ja", "Man kan vel si det ja", "Ehm, tror det er best vi ikke snakker om det jeg :sweat_smile:", "нет", "Nei ass", "Er ikke så sannsynlig", "I følge mine beregninger... nei"]
        await ctx.send(random.choice(answers))


    @commands.cooldown(1, 2, commands.BucketType.guild)
    @commands.command(aliases=["reverse"])
    async def reverser(self, ctx, *, tekst):
        """Reverserer tekst"""

        embed = discord.Embed(color=0x0085ff)
        embed.add_field(name="Reversert tekst", value=tekst[::-1])
        await ctx.send(embed=embed)


    @commands.cooldown(1, 5, commands.BucketType.guild)
    @commands.command(aliases=["owoify", "uwu"])
    async def owo(self, ctx, *setning):
        """Oversetter teksten din til owo"""

        embed = discord.Embed(description="Laster...")
        statusmsg = await ctx.send(embed=embed)

        #   Sjekk for error & Hent data
        try:
            data = requests.get(f"https://nekos.life/api/v2/owoify?text={setning}").json()

            owoRaw = str(data["owo"][2:-2])
            owo = owoRaw.replace(",", "").replace("'", "")

            embed = discord.Embed(color=0x0085ff)
            embed.add_field(name="OwO", value=owo)
            await statusmsg.edit(embed=embed)

        except:
            embed = discord.Embed(color=0xFF0000, description=":x: oopsie whoopsie you made a fucky wucky, no text or text over 200")
            await statusmsg.edit(embed=embed)
    

    @commands.cooldown(1, 5, commands.BucketType.guild)
    @commands.command(aliases=["urban", "meaning", "mening", "betydning", "dictionary", "ordbok"])
    async def urbandictionary(self, ctx, *ord):
        """Sjekk definisjonen av et ord"""

        embed = discord.Embed(description="Laster...")
        statusmsg = await ctx.send(embed=embed)

        #   Sjekk for error
        try:
            data = requests.get(f"https://api.urbandictionary.com/v0/define?term={ord}").json()
            definitionUrl = data["list"][0]["permalink"]

        except:
            embed = discord.Embed(color=0xFF0000, description=f":x: Noe gikk galt\n\nSkriv `{prefix}help urban` for hjelp")
            await statusmsg.edit(embed=embed)
            return

        #   Hent restn av data
        word = data["list"][0]["word"]
        submitter = data["list"][0]["author"]

        de = data["list"][0]["definition"]
        definition = de.replace("[", "").replace("]", "").replace(";", "")
        ex = data["list"][0]["example"]
        example = ex.replace("[", "").replace("]", "").replace(";", "")

        thumbsUp = data["list"][0]["thumbs_up"]
        thumbsDown = data["list"][0]["thumbs_down"]
        
        #   Embed
        embed = discord.Embed(title=word, color=0x0085ff, url=definitionUrl, description= f"**Definert av:** {submitter}")
        embed.set_author(name="Urban Dictionary", icon_url="https://a2.mzstatic.com/us/r30/Purple/v4/dd/ef/75/ddef75c7-d26c-ce82-4e3c-9b07ff0871a5/mzl.yvlduoxl.png")
        embed.set_footer(text=f"{ctx.message.author.name}#{ctx.message.author.discriminator}", icon_url=ctx.message.author.avatar_url)
        embed.add_field(name="Definisjon", value=definition)
        embed.add_field(name="Eksempel", value=example)
        embed.add_field(name="Vurdering", value=f":thumbsup: {thumbsUp} / :thumbsdown: {thumbsDown}", inline=False)
        await statusmsg.edit(embed=embed)
        

def setup(bot):
    bot.add_cog(Misc(bot))