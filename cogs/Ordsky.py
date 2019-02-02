import discord
import asyncio
from discord.ext import commands

import os
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

        statusmsg = await ctx.send(f"{ctx.message.author.mention}\n**Teller ord:** :hourglass:\n**Generer ordsky:** -")

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
        
        #   Skyform
        if skyform == "ostehøvel":
            maskbilde = np.array(Image.open("./assets/ordsky/mask/ostmask.png"))
        elif skyform == "laugh":
            maskbilde = np.array(Image.open("./assets/ordsky/mask/laughmask.png"))

        elif ctx.message.attachments != [] and skyform == None:
            try:
                await ctx.message.attachments[0].save(fp=f"{ctx.message.author.id}_mask.png")
                maskbilde = np.array(Image.open(f"{ctx.message.author.id}_mask.png"))
            except:
                await statusmsg.edit(content="Feilet henting av skyform")
                return

        else:
            maskbilde = np.array(Image.open("./assets/ordsky/mask/owomask.png"))

        await statusmsg.edit(content=f"{ctx.message.author.mention}\n**Teller ord:** :white_check_mark:\n**Generer ordsky:** :hourglass:")

        #   Ordsky innstillinger
        wc = WordCloud(font_path=None, max_words=4000, mask=maskbilde)

        #   Generer ordsky
        wc.generate(text)

        #   Fargelegg
        if  ctx.message.attachments != [] or skyform == "laugh":
            image_colors = ImageColorGenerator(maskbilde)
            wc.recolor(color_func=image_colors)

        #   Lagre bilde
        wc.to_file(f"./assets/ordsky/bilde/{ctx.message.author.id}.png")

        #   Send bilde
        await ctx.send(f":white_check_mark: Generert ordsky for <@{ctx.message.author.id}>", file=discord.File(f"./assets/ordsky/bilde/{ctx.message.author.id}.png"))
        
        #   Cleanup, sletting
        await statusmsg.delete()
        
        try:
            os.remove(f"./{ctx.message.author.id}_mask.png")
        except:
            pass


def setup(bot):
    bot.add_cog(Ordsky(bot))