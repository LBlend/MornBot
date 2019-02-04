import discord
import asyncio
from discord.ext import commands

import os
import urllib.request
from PIL import Image
import numpy as np
from wordcloud import WordCloud, ImageColorGenerator


class Ordsky:
    def __init__(self, bot):
        self.bot = bot


    @commands.cooldown(1, 300, commands.BucketType.user)
    @commands.command(aliases=["wordcloud", "wc", "sky"])
    async def ordsky(self, ctx, skyform=None):
        """Generer en ordsky"""

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
                    return
                maskbilde = np.array(Image.open(f"{ctx.message.author.id}_mask.png"))
            except:
                embed = discord.Embed(color=0xFF0000, description=":x: **Stoppet!**\n\nFeilet henting av skyform")
                await statusmsg.edit(content=ctx.message.author.mention, embed=embed)
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
                    return
                maskbilde = np.array(Image.open(f"{ctx.message.author.id}_mask.png"))
            except:
                embed = discord.Embed(color=0xFF0000, description=":x: **Stoppet!**\n\nFeilet henting av skyform")
                await statusmsg.edit(content=ctx.message.author.mention, embed=embed)
                return

        else:
            maskbilde = np.array(Image.open("./assets/ordsky/mask/owomask.png"))

        #   Søk etter ord
        text = ""
        for channel in ctx.message.guild.text_channels:
            async for message in channel.history(limit=4000):
                if message.author.id == ctx.message.author.id:
                    try:
                        text += f"{message.content} "
                    except:
                        pass
                else:
                    pass

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


def setup(bot):
    bot.add_cog(Ordsky(bot))