import discord
import asyncio
from discord.ext import commands

import codecs
import json
from pathlib import Path
import os
import urllib.request
from PIL import Image
import numpy as np
from wordcloud import WordCloud, ImageColorGenerator


with codecs.open("config.json", "r", encoding="utf8") as f:
    config = json.load(f)
    prefix = config["prefix"]


class Ordsky:
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

        userMessages = Path(f"./assets/ordsky/tekst/{ctx.message.author.id}.txt")
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
            await ctx.message.author.send(file=discord.File(f"./assets/ordsky/tekst/{ctx.message.author.id}.txt"))
            embed = discord.Embed(color=0x0085ff, description=f":white_check_mark: Meldingsdata har blitt sendt i DM!")
        except:
            embed = discord.Embed(color=0xF1C40F, description=":exclamation: Jeg har ingen data om deg å sende!")

        await ctx.send(embed=embed)


    @commands.cooldown(1, 150, commands.BucketType.user)
    @commands.command(aliases=["wordcloud", "wc", "sky"])
    async def ordsky(self, ctx, skyform=None):
        """Generer en ordsky"""

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


        embed = discord.Embed(description="**Teller ord:** :hourglass:\n**Generer ordsky:** -")
        statusmsg = await ctx.send(ctx.message.author.mention, embed=embed)
        
        #   Skyform
        if skyform == "ostehøvel":
            maskbilde = np.array(Image.open("./assets/ordsky/mask/ostmask.png"))
        elif skyform == "laugh":
            maskbilde = np.array(Image.open("./assets/ordsky/mask/laughmask.png"))

        elif ctx.message.attachments != [] and skyform == None:
            try:
                await ctx.message.attachments[0].save(fp=f"{ctx.message.author.id}_mask.png")
                filesize = os.path.getsize(f"{ctx.message.author.id}_mask.png")
                if filesize > 2000000:
                    embed = discord.Embed(color=0xFF0000, description=":x: **Stoppet!**\n\nFilen er for stor. Prøv en fil som er mindre enn 2 MiB")
                    await statusmsg.edit(content=ctx.message.author.mention, embed=embed)
                    try:
                        os.remove(f"./{ctx.message.author.id}_mask.png")
                    except:
                        pass
                    self.bot.get_command("ordsky").reset_cooldown(ctx)
                    return
                maskbilde = np.array(Image.open(f"{ctx.message.author.id}_mask.png"))
            except:
                embed = discord.Embed(color=0xFF0000, description=":x: **Stoppet!**\n\nFeilet henting av skyform")
                await statusmsg.edit(content=ctx.message.author.mention, embed=embed)
                self.bot.get_command("ordsky").reset_cooldown(ctx)
                return
        elif  ctx.message.attachments == [] and skyform != None:
            try:
                urllib.request.urlretrieve(str(skyform), f"{ctx.message.author.id}_mask.png")
                filesize = os.path.getsize(f"{ctx.message.author.id}_mask.png")
                if filesize > 2000000:
                    embed = discord.Embed(color=0xFF0000, description=":x: **Stoppet!**\n\nFilen er for stor. Prøv en fil som er mindre enn 2 MiB")
                    await statusmsg.edit(content=ctx.message.author.mention, embed=embed)
                    try:
                        os.remove(f"./{ctx.message.author.id}_mask.png")
                    except:
                        pass
                    self.bot.get_command("ordsky").reset_cooldown(ctx)
                    return
                maskbilde = np.array(Image.open(f"{ctx.message.author.id}_mask.png"))
            except:
                embed = discord.Embed(color=0xFF0000, description=":x: **Stoppet!**\n\nFeilet henting av skyform")
                await statusmsg.edit(content=ctx.message.author.mention, embed=embed)
                self.bot.get_command("ordsky").reset_cooldown(ctx)
                return

        else:
            maskbilde = np.array(Image.open("./assets/ordsky/mask/owomask.png"))

        #   Søk etter ord
        """NEEDS TO BE REWRITTEN. TEMPORARY SOLUTION"""
        userMessages = Path(f"./assets/ordsky/tekst/{ctx.message.author.id}_{ctx.message.server.id}.txt")
        if userMessages.is_file() == False:
            with codecs.open(f"./assets/ordsky/tekst/{ctx.message.author.id}_{ctx.message.server.id}.txt", "a+") as f:
                for channel in ctx.message.guild.text_channels:
                    async for message in channel.history(limit=4000):
                        if message.author.id == ctx.message.author.id:
                            try:
                                f.write(f"{message.content} ")
                            except:
                                pass
                        else:
                            pass

        else:
            with codecs.open(f"./assets/ordsky/tekst/{ctx.message.author.id}_{ctx.message.server.id}.txt", "a+") as f:
                for channel in ctx.message.guild.text_channels:
                    async for message in channel.history(limit=300):
                        if message.author.id == ctx.message.author.id:
                            try:
                                f.write(f"{message.content} ")
                            except:
                                pass
                        else:
                            pass

        text = open(f"./assets/ordsky/tekst/{ctx.message.author.id}_{ctx.message.server.id}.txt").read()

        await statusmsg.edit(content=ctx.message.author.mention)
        embed = discord.Embed(description="**Teller ord:** :white_check_mark:\n**Generer ordsky:** :hourglass:")
        await statusmsg.edit(content=ctx.message.author.mention, embed=embed)

        #   Ordsky innstillinger
        wc = WordCloud(font_path=None, max_words=4000, mask=maskbilde)

        #   Generer ordsky
        wc.generate(text)

        #   Fargelegg
        if  ctx.message.attachments != [] or skyform == "laugh":
            image_colors = ImageColorGenerator(maskbilde)
            wc.recolor(color_func=image_colors)
        elif ctx.message.attachments == [] and skyform != None:
            image_colors = ImageColorGenerator(maskbilde)
            wc.recolor(color_func=image_colors)

        #   Lagre bilde
        wc.to_file(f"./assets/ordsky/bilde/{ctx.message.author.id}.png")

        #   Send bilde
        await ctx.send(f":white_check_mark: Generert ordsky for {ctx.message.author.mention}", file=discord.File(f"./assets/ordsky/bilde/{ctx.message.author.id}.png"))

        #   Cleanup, sletting
        await statusmsg.delete()
        
        try:
            os.remove(f"./{ctx.message.author.id}_mask.png")
        except:
            pass
        try:
            os.remove(f"./assets/ordsky/bilde/{ctx.message.author.id}.png")
        except:
            pass


def setup(bot):
    bot.add_cog(Ordsky(bot))