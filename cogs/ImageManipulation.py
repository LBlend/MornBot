import discord
import asyncio
from discord.ext import commands

import urllib.request
import os
import PIL
from PIL import Image


class ImageManipulation:
    def __init__(self, bot):
        self.bot = bot


    @commands.cooldown(1, 5, commands.BucketType.guild)
    @commands.command(aliases=["needsmorejpeg", "jpg", "jpeg"])
    async def needsmorejpg(self, ctx, bilde=None):
        """Bruk denne kommandoen for å vise alle 
        hvorfor jpg er det beste bildeformatet"""

        #   Statusmelding
        embed = discord.Embed(description="JPG-ifiserer...")
        statusmsg = await ctx.send(embed=embed)

        #   Hent bilde
        if ctx.message.attachments != []:
            await ctx.message.attachments[0].save(fp=f"./assets/{ctx.message.author.id}_notjpged.png")
        else:
            try:
                urllib.request.urlretrieve(str(bilde), f"./assets/{ctx.message.author.id}_notjpged.png")
            except:
                embed = discord.Embed(color=0xFF0000, description=":x: Henting av bilde feilet")
                await ctx.send(content=ctx.message.author.mention, embed=embed)
                await statusmsg.delete()
                return

        rawimage = Image.open(f"./assets/{ctx.message.author.id}_notjpged.png")
        rawimageNonRGB = rawimage.convert("RGB") 
        rawimageNonRGB.save(f"./assets/{ctx.message.author.id}_jpged.jpg", quality=5)

        f = discord.File(f"./assets/{ctx.message.author.id}_jpged.jpg")
        await ctx.send(file=f)
        await statusmsg.delete()

        try:
            os.remove(f"./assets/{ctx.message.author.id}_notjpged.png")
        except:
            pass
        try:
            os.remove(f"./assets/{ctx.message.author.id}_jpged.jpg")
        except:
            pass


def setup(bot):
    bot.add_cog(ImageManipulation(bot))