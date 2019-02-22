import discord
import asyncio
from discord.ext import commands

import urllib
import requests
import os
import PIL
from PIL import Image

async def fileFetchFail(ctx, statusmsg):
    embed = discord.Embed(color=0xFF0000, description=":x: Henting av bilde feilet")
    await statusmsg.edit(content=ctx.message.author.mention, embed=embed)

async def fileTooBig(ctx, statusmsg, fileSize):
    embed = discord.Embed(color=0xFF0000, description=f":x: **Stoppet!**\n\nFilen er for stor. Prøv en fil som er mindre enn {fileSize}")
    await statusmsg.edit(content=ctx.message.author.mention, embed=embed)

async def noFile(ctx, statusmsg):
    embed = discord.Embed(color=0xF1C40F, description=f":exclamation: nDu må gi meg et bilde")
    await statusmsg.edit(content=ctx.message.author.mention, embed=embed)


class ImageManipulation:
    def __init__(self, bot):
        self.bot = bot


    @commands.cooldown(1, 5, commands.BucketType.guild)
    @commands.command(aliases=["needsmorejpeg", "jpg", "jpeg"])
    async def needsmorejpg(self, ctx, bilde=None):

        #   Statusmelding
        embed = discord.Embed(description="JPG-ifiserer...")
        statusmsg = await ctx.send(embed=embed)

        #   Hent bilde
        if ctx.message.attachments != [] and bilde == None:
            if ctx.message.attachments[0].size > 8000000:
                await fileTooBig(ctx, statusmsg, fileSize="8 MiB")
                return
            try:
                await ctx.message.attachments[0].save(fp=f"./assets/{ctx.message.author.id}_notjpged.png")
            except:
                await fileFetchFail(ctx, statusmsg)
                return
        
        elif ctx.message.attachments == [] and bilde != None:
            try:
                linkedFile = requests.get(str(bilde))
                linkedFileSize = len(linkedFile.content)
            except:
                await fileFetchFail(ctx, statusmsg)
                return

            if linkedFileSize > 8000000:
                await fileTooBig(ctx, statusmsg, fileSize="8 MiB")
                return

            try:
                urllib.request.urlretrieve(str(bilde), f"./assets/{ctx.message.author.id}_notjpged.png")
            except:
                await fileFetchFail(ctx, statusmsg)
                return

        else:
            await noFile(ctx, statusmsg)
            return

        #   JPG-ifiser
        rawimage = Image.open(f"./assets/{ctx.message.author.id}_notjpged.png")
        rawimageNonRGB = rawimage.convert("RGB") 
        rawimageNonRGB.save(f"./assets/{ctx.message.author.id}_jpged.jpg", quality=5)

        f = discord.File(f"./assets/{ctx.message.author.id}_jpged.jpg")
        await ctx.send(file=f)
        await statusmsg.delete()

        #   Cleanup, sletting
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