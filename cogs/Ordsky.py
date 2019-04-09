import discord
import asyncio
from discord.ext import commands

import codecs
import json
from pathlib import Path
import os
from PIL import Image
import numpy as np
from wordcloud import WordCloud
import re

with codecs.open("config.json", "r", encoding="utf8") as f:
    config = json.load(f)
    prefix = config["prefix"]


class Ordsky(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.cooldown(1, 2, commands.BucketType.user)
    @commands.command(aliases=["consent"])
    async def samtykke(self, ctx):
        """Gi samtykke til å samle meldingsdataen din"""
    
        userDataFile = Path(f"./assets/userdata/{ctx.message.author.id}.json")
        if userDataFile.is_file() == False:
            with codecs.open(f"./assets/userdata/{ctx.message.author.id}.json", "w") as f:
                json.dump({"name": f"{ctx.message.author.name}#{ctx.message.author.discriminator}", "consent": True}, f)
            
        else:
            """NEEDS TO BE REWRITTEN. TEMPORARY SOLUTION"""
            with codecs.open(f"./assets/userdata/{ctx.message.author.id}.json", "r+") as f:
                userData = json.load(f)
                userData["consent"] = True
                with codecs.open(f"./assets/userdata/{ctx.message.author.id}.json", "w") as f2:
                    f2.seek(0)
                    f2.write(json.dumps(userData))
        
        embed = discord.Embed(color=0x0085ff, description=f":white_check_mark: Samtykke registrert!")
        await ctx.send(embed=embed)


    @commands.cooldown(1, 2, commands.BucketType.user)
    @commands.command(aliases=["ingensamtykke", "noconsent"])
    async def tabort(self, ctx):
        """Ta bort samtykken din om samling av meldingsdata"""

        userDataFile = Path(f"./assets/userdata/{ctx.message.author.id}.json")
        if userDataFile.is_file() == False:
            with codecs.open(f"./assets/userdata/{ctx.message.author.id}.json", "w") as f:
                json.dump({"name": f"{ctx.message.author.name}#{ctx.message.author.discriminator}", "consent": False}, f)

        else:
            with codecs.open(f"./assets/userdata/{ctx.message.author.id}.json", "r+") as f:
                userData = json.load(f)
                userData["consent"] = False
                f.seek(0)
                f.write(json.dumps(userData))  

        userMessages = Path(f"./assets/ordsky/tekst/{ctx.message.author.id}_{ctx.message.guild.id}.txt")

        try:
            os.remove(userMessages)
        except:
            pass

        embed = discord.Embed(color=0x0085ff, description=f":white_check_mark: Meldingsdata er slettet!")
        await ctx.send(embed=embed)


    @commands.cooldown(1, 60, commands.BucketType.user)
    @commands.command(aliases=["mydata"])
    async def minedata(self, ctx):
        """Få tilsendt dine data"""

        try:
            await ctx.message.author.send(file=discord.File(f"./assets/ordsky/tekst/{ctx.message.author.id}_{ctx.message.guild.id}.txt"))
            embed = discord.Embed(color=0x0085ff, description=f":white_check_mark: Meldingsdata har blitt sendt i DM!")
        except:
            embed = discord.Embed(color=0xF1C40F, description=":exclamation: Jeg har ingen data om deg å sende eller så kan jeg ikke sende meldinger til deg!")

        await ctx.send(embed=embed)


    @commands.cooldown(1, 150, commands.BucketType.user)
    @commands.command(aliases=["wordcloud", "wc", "sky"])
    async def ordsky(self, ctx):
        """Generer en ordsky"""

        #   Sjekk samtykke
        userDataFile = Path(f"./assets/userdata/{ctx.message.author.id}.json")
        if userDataFile.is_file() == False:
            with codecs.open(f"./assets/userdata/{ctx.message.author.id}.json", "w") as f:
                json.dump({"name": f"{ctx.message.author.name}#{ctx.message.author.discriminator}", "consent": False}, f)
      
        with codecs.open(f"./assets/userdata/{ctx.message.author.id}.json", "r", encoding="utf8") as f:
            userData = json.load(f)
            consent = userData["consent"]

        if consent == False:
            embed = discord.Embed(color=0xF1C40F, description=f":exclamation: Du må gi meg tillatelse til å samle og beholde meldingsdataene dine.\n\nSkriv `{prefix}samtykke` for å gjøre dette")
            statusmsg = await ctx.send(ctx.message.author.mention, embed=embed)
            self.bot.get_command("ordsky").reset_cooldown(ctx)
            return

        #   Statusmelding
        embed = discord.Embed(description="**Teller ord:** :hourglass:\n**Generer ordsky:** -")
        embed.set_footer(icon_url=ctx.message.author.avatar_url, text=f"{ctx.message.author.name}#{ctx.author.discriminator}")
        statusmsg = await ctx.send(ctx.message.author.mention, embed=embed)

        #   Søk etter ord
        """NEEDS TO BE REWRITTEN. TEMPORARY SOLUTION"""
        userMessages = Path(f"./assets/ordsky/tekst/{ctx.message.author.id}_{ctx.message.guild.id}.txt")
        if userMessages.is_file() == False:
            with codecs.open(f"./assets/ordsky/tekst/{ctx.message.author.id}_{ctx.message.guild.id}.txt", "a+") as f:
                try:
                    for channel in ctx.message.guild.text_channels:
                        for message in channel.history(limit=2000):
                            if message.author.id == ctx.message.author.id:
                                try:
                                    f.write(f"{message.content} ")
                                except:
                                    pass
                            else:
                                pass
                except:
                    pass

        else:
            with codecs.open(f"./assets/ordsky/tekst/{ctx.message.author.id}_{ctx.message.guild.id}.txt", "a+") as f:
                try:
                    for channel in ctx.message.guild.text_channels:
                        for message in channel.history(limit=300):
                            if message.author.id == ctx.message.author.id:
                                try:
                                    f.write(f"{message.content} ")
                                except:
                                    pass
                            else:
                                pass
                except:
                    pass

        await statusmsg.edit(content=ctx.message.author.mention)
        embed = discord.Embed(description="**Teller ord:** :white_check_mark:\n**Generer ordsky:** :hourglass:")
        embed.set_footer(icon_url=ctx.message.author.avatar_url, text=f"{ctx.message.author.name}#{ctx.author.discriminator}")
        await statusmsg.edit(content=ctx.message.author.mention, embed=embed)

        #   Tekstfiltrering
        text = open(f"./assets/ordsky/tekst/{ctx.message.author.id}_{ctx.message.guild.id}.txt").read()
        text = re.sub(r'http\S+', '', text)

        """UHHHHHHHM DON'T THINK ABOUT IT OK?"""
        filteredWords = ["og","i","det","på","som","er","en","til","å","han","av","for","med","at","var","de","ikke","den","har","jeg","om","et","men","så","seg","hun","hadde","fra","vi","du","kan","da","ble","ut","skal","vil","ham","etter","over","ved","også","bare","eller","sa","nå","dette","noe","være","meg","mot","opp","der","når","inn","dem","kunne","andre","blir","alle","noen","sin","ha","år","henne","må","selv","sier","få","kom","denne","enn","to","hans","bli","ville","før","vært","skulle","går","her","slik","gikk","mer","hva","igjen","fikk","man","alt","mange","ingen","får","oss","hvor","under","siden","hele","dag","gang","sammen","ned","kommer","sine","deg","se","første","godt","mellom","måtte","gå","helt","litt","nok","store","aldri","ta","sig","uten","ho","kanskje","blitt","ser","hvis","vel","si","vet","hennes","min","tre","ja","samme","mye","nye","tok","gjøre","disse","rundt","tilbake","mens","satt","flere","folk","fordi","både","la","gjennom","fått","like","nei","annet","komme","gjorde","hvordan","sånn","dere","jo"]

        #   Skyform
        maskbilde = np.array(Image.open("./assets/ordsky/mask/skyform.png"))

        #   Ordsky innstillinger
        wc = WordCloud(font_path=None, max_words=4000, mask=maskbilde, repeat=True, stopwords=filteredWords)

        #   Mer tekstfiltrering
        wc.process_text(text)

        #   Generer ordsky
        try:
            wc.generate(text)
        except:
            embed = discord.Embed(color=0xFF0000, description=":x: Generering av ordsky feilet")
            await ctx.send(content=ctx.message.author.mention, embed=embed)
            await statusmsg.delete()

        #   Lagre bilde
        wc.to_file(f"./assets/ordsky/bilde/{ctx.message.author.id}.png")

        #   Send bilde
        await ctx.send(f":white_check_mark: Generert ordsky for {ctx.message.author.mention}", file=discord.File(f"./assets/ordsky/bilde/{ctx.message.author.id}.png"))

        #   Cleanup, sletting
        await statusmsg.delete()
        try:
            os.remove(f"./assets/ordsky/bilde/{ctx.message.author.id}.png")
        except:
            pass


def setup(bot):
    bot.add_cog(Ordsky(bot))