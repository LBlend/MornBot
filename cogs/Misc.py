import discord
import asyncio
from discord.ext import commands

import codecs
import json
import requests
import random
from hashlib import md5
from bs4 import BeautifulSoup
from datetime import datetime
import re

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

    @commands.cooldown(1, 5, commands.BucketType.guild)
    @commands.command(aliases=["bakgrunn"])
    async def wallpaper(self, ctx):
        """Sender et tilfeldig bakgrunnsbilde (NSFW)"""

        embed = discord.Embed(description="Laster...")
        statusmsg = await ctx.send(embed=embed)

        #   Sjekk NSFW
        if not ctx.channel.is_nsfw():
            embed = discord.Embed(color=0xFF0000, description=":x: Du må være i en NSFW-kanal")
            await statusmsg.edit(embed=embed)
            return

        #   Hent data
        data = requests.get("https://nekos.life/api/v2/img/wallpaper").json()
        wallpaper = data["url"]

        #   Embed
        embed = discord.Embed(color=0x0085ff)
        embed.set_image(url=wallpaper)
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

        embed = discord.Embed(description="Laster...")
        statusmsg = await ctx.send(embed=embed)

        if tekst is None or len(tekst) >= 1000:
            embed = discord.Embed(color=0xFF0000, description=":x: Teksten er enten for lang eller så har du ikke gitt noe tekst")
            await statusmsg.edit(embed=embed)
            return

        embed = discord.Embed(color=0x0085ff, description=tekst[::-1])
        embed.set_footer(text=f"{ctx.message.author.name}#{ctx.message.author.discriminator}", icon_url=ctx.message.author.avatar_url)
        await statusmsg.edit(embed=embed)


    @commands.cooldown(1, 2, commands.BucketType.guild)
    @commands.command(aliases=["owoify", "uwu"])
    async def owo(self, ctx, *tekst):
        """Oversetter teksten din til owo"""

        embed = discord.Embed(description="Laster...")
        statusmsg = await ctx.send(embed=embed)

        if not tekst or len(tekst) >= 1000:
            embed = discord.Embed(color=0xFF0000, description=":x: oopsie whoopsie you made a fucky wucky. Teksten er enten for lang eller så har du ikke gitt noe tekst")
            await statusmsg.edit(embed=embed)
            return

        tekst = re.sub("'|,", "", str(tekst))
        tekst = re.sub("r|l", "w", tekst)
        tekst = re.sub("R|L", "W", tekst)
        tekst = re.sub("n[aeiou]", "ny", tekst)
        tekst = re.sub("N[aeiou]", "Ny", tekst)
        tekst = re.sub("N[AEIOU]", "Ny", tekst)
        tekst = re.sub("ove", "uv", tekst)
        #tekst = re.sub("!", " (・`ω´・)", tekst) #https://kaomoji.moe/

        embed = discord.Embed(color=0x0085ff, description=tekst[1:-1])
        embed.set_footer(text=f"{ctx.message.author.name}#{ctx.message.author.discriminator}", icon_url=ctx.message.author.avatar_url)
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
        embed.set_footer(text=f"{ctx.message.author.name}#{ctx.message.author.discriminator}", icon_url=ctx.message.author.avatar_url)
        await statusmsg.edit(embed=embed)

    
    @commands.cooldown(1, 10, commands.BucketType.guild)
    @commands.command(aliases=["isitdown", "checksite"])
    async def isitup(self, ctx, nettside: str):
        """Sjekk om en nettside er oppe"""

        embed = discord.Embed(description="Laster...")
        statusmsg = await ctx.send(embed=embed)

        data = requests.get(f"https://isitup.org/{nettside}")
        scrapedData = BeautifulSoup(data.text, "html.parser")
        status = scrapedData.find("p").get_text()
        nettside = scrapedData.find(class_="domain").get_text()
        nettsideLink = scrapedData.find(class_="domain")["href"]

        embed = discord.Embed(title=nettside.capitalize(), url=nettsideLink, timestamp=datetime.utcnow())

        if status[-6:] == "is up.":
            status = "Oppe!"
            ping = scrapedData.find(class_="smaller").get_text()
            pinglist = []
            for i in ping.split():
                if i.isdigit():
                    pinglist.append(i)
            embed.add_field(name="Ping", value=f"{pinglist[0]} ms")
            embed.color = 0x2ECC71
        else:
            status = "Nede!"
            embed.color = 0xff0000

        embed.add_field(name="Status", value=status)
        await statusmsg.edit(embed=embed)

    
    @commands.cooldown(1, 2, commands.BucketType.guild)
    @commands.command(aliases=["clapify"])
    async def klappifiser(self, ctx, *tekst):
        """Klapppifiserer teksten din"""

        embed = discord.Embed(description="Laster...")
        statusmsg = await ctx.send(embed=embed)

        if not tekst or len(tekst) >= 1000:
            embed = discord.Embed(color=0xFF0000, description=":x: Teksten er enten for lang eller så har du ikke gitt noe tekst")
            await statusmsg.edit(embed=embed)
            return

        tekst = re.sub("'|,", "", str(tekst).upper())
        tekst = re.sub(" ", "👏", tekst)

        embed = discord.Embed(color=0x0085ff, description=f"👏**{tekst[1:-1]}**👏")
        embed.set_footer(text=f"{ctx.message.author.name}#{ctx.message.author.discriminator}", icon_url=ctx.message.author.avatar_url)
        await statusmsg.edit(embed=embed)


    @commands.guild_only()
    @commands.cooldown(1, 2, commands.BucketType.guild)
    @commands.command(aliases=["video"])
    async def videochat(self, ctx):
        """Få link til videochat"""

        try:
            voiceChannelId = ctx.author.voice.channel.id
        except:
            embed = discord.Embed(color=0xFF0000, description=":x: Du må være koblet til en talekanal")
            await ctx.send(embed=embed)
            return

        link = f"https://canary.discordapp.com/channels/{ctx.guild.id}/{voiceChannelId}"
        embed = discord.Embed(color=0x0085ff, title=f"Videochat: {ctx.author.voice.channel.name}", description=f"[Trykk her for å bli med i videochat]({link})")
        await ctx.send(embed=embed)

    
    @commands.cooldown(1, 5, commands.BucketType.guild)
    @commands.command(aliases=["timezone", "tid", "tidssone", "klokken"])
    async def klokka(self, ctx, kontinent, by):
        """Se hvor mye klokka er i et bestemt område"""

        embed = discord.Embed(description="Laster...")
        statusmsg = await ctx.send(embed=embed)

        try:
            data = requests.get(f"http://worldtimeapi.org/api/timezone/{kontinent.capitalize()}/{by.capitalize()}").json()
            timezone = data["timezone"]
        except:
            embed = discord.Embed(color=0xFF0000, description=f":x: Fant ikke sted\n\nSkriv `{prefix}help klokka` for hjelp")
            await statusmsg.edit(embed=embed)
            return

        timezone = re.split("/", timezone)
        localTimezone = data["abbreviation"]
        utcTimezone = data["utc_offset"]
        norwayTime = datetime.now().strftime("%H:%M\n%d.%m.%Y")

        time = data["datetime"]
        timeFormatted = f"{time[11:16]}\n{time[8:10]}.{time[5:7]}.{time[:4]}"

        daylightSavings = data["dst"]
        if daylightSavings is False:
            daylightSavings = "Nei"
        else:
            daylightSavings = "Ja"

        #   Embed
        embed = discord.Embed(title=f"Klokka i {timezone[1]}", color=0x0085ff, timestamp=datetime.utcnow())
        embed.add_field(name="Klokka", value=timeFormatted)
        embed.add_field(name="Klokka i Norge", value=norwayTime)
        embed.add_field(name="Sommertid", value=daylightSavings)
        embed.add_field(name="UTC tidssone", value=utcTimezone)
        embed.add_field(name="Standard tidssone for sted", value=localTimezone)
        embed.set_footer(text="Klokka i din tidssone ->")
        
        await statusmsg.edit(embed=embed)
 
        

def setup(bot):
    bot.add_cog(Misc(bot))