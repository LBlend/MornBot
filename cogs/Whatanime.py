import discord
import asyncio
from discord.ext import commands

import base64
import requests
import urllib.request
import os
from datetime import timedelta
import PIL
from PIL import Image

async def fileFetchFail(ctx, statusmsg):
    embed = discord.Embed(color=0xFF0000, description=":x: Henting av bilde feilet")
    await statusmsg.edit(content=ctx.message.author.mention, embed=embed)

async def fileTooBig(ctx, statusmsg, fileSize):
    embed = discord.Embed(color=0xFF0000, description=f":x: **Stoppet!**\n\nFilen er for stor. Prøv en fil som er mindre")
    await statusmsg.edit(content=ctx.message.author.mention, embed=embed)

async def noFile(ctx, statusmsg):
    embed = discord.Embed(color=0xF1C40F, description=f":exclamation: Du må gi meg et bilde")
    await statusmsg.edit(content=ctx.message.author.mention, embed=embed)


class Whatanime(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.cooldown(1, 10, commands.BucketType.guild)
    @commands.command(aliases=["anime", "ani", "source", "saus", "sauce"])
    async def whatanime(self, ctx, bilde=None):
        """Finner ut hvilken anime et skjermbilde er tatt fra"""

        embed = discord.Embed(description="Finner saus... :mag_right:")
        statusmsg = await ctx.send(embed=embed)

        if ctx.message.attachments != [] and bilde == None:
            if ctx.message.attachments[0].size > 8000000:
                await fileTooBig(ctx, statusmsg, fileSize="8 MiB")
                return
            try:
                await ctx.message.attachments[0].save(fp=f"./assets/{ctx.message.author.id}_trace.png")
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
                urllib.request.urlretrieve(str(bilde), f"./assets/{ctx.message.author.id}_trace.png")
            except:
                await fileFetchFail(ctx, statusmsg)
                return

        else:
            await noFile(ctx, statusmsg)
            return

        filesize = os.path.getsize(f"./assets/{ctx.message.author.id}_trace.png")
        if filesize > 1000000:
            basewidth = 300
            img = Image.open(f"./assets/{ctx.message.author.id}_trace.png")
            wpercent = (basewidth / float(img.size[0]))
            hsize = int((float(img.size[1]) * float(wpercent)))
            img = img.resize((basewidth, hsize), Image.ANTIALIAS)
            img.save(f"./assets/{ctx.message.author.id}_trace.png")

            newFilesize = os.path.getsize(f"./assets/{ctx.message.author.id}_trace.png")
            if newFilesize > 1000000:
                await fileTooBig(ctx, statusmsg, fileSize=None)
                os.remove(f"./assets/{ctx.message.author.id}_trace.png")
                return

        with open(f"./assets/{ctx.message.author.id}_trace.png", "rb") as f:
            base = base64.standard_b64encode(f.read())
            try:
                data = requests.post("https://trace.moe/api/search", data={'image': base}).json()
            except:
                embed = discord.Embed(color=0xF1C40F, description=":exclamation: Ingen saus ble funnet")
                await ctx.send(content=ctx.message.author.mention, embed=embed)
                await statusmsg.delete()
                os.remove(f"./assets/{ctx.message.author.id}_trace.png")
                return

        similarity = data["docs"][0]["similarity"]
        if similarity < 0.85:
            embed = discord.Embed(color=0xF1C40F, description=":exclamation: Saus ble funnet, men grunnet lav likhetsprosent, er det høy sannsynlighet for at dette ikke er riktig saus. Vennligst prøv et annet bilde")
            await ctx.send(content=ctx.message.author.mention, embed=embed)
            await statusmsg.delete()
            os.remove(f"./assets/{ctx.message.author.id}_trace.png")
            return

        anilistId = data["docs"][0]["anilist_id"]
        malId = data["docs"][0]["mal_id"]
        romajiTitle = data["docs"][0]["title_romaji"]
        nativeTitle = data["docs"][0]["title_native"]
        englishTitle = data["docs"][0]["title_english"]
        episode = data["docs"][0]["episode"]
        time = int(data["docs"][0]["at"])

        malData = requests.get(f"https://api.jikan.moe/v3/anime/{malId}/pictures").json()
        thumbnail = malData["pictures"][0]["small"]

        similarity_percent = round(similarity * 100, 2)
        formattedTime = timedelta(seconds=time)
        if episode == "":
            episode = "0 (Film)"

        try:
            embed = discord.Embed(title=romajiTitle, color=0x0085ff, url=f"https://anilist.co/anime/{anilistId}")
            embed.set_thumbnail(url=thumbnail)
            embed.set_author(name=ctx.message.author.name, icon_url=ctx.message.author.avatar_url)
            embed.description = f"{nativeTitle}\n{englishTitle}"
            embed.add_field(name="Episode", value=str(episode))
            embed.add_field(name="Tidspunkt", value=str(formattedTime))
            embed.add_field(name="Likhet %", value=f"{similarity_percent}%")
            embed.add_field(name="Lenker", value=f"[MAL](https://myanimelist.net/anime/{malId}) | [Anilist](https://anilist.co/anime/{anilistId})")

            await ctx.send(content=ctx.message.author.mention, embed=embed)
            await statusmsg.delete()

        except:
            embed = discord.Embed(color=0xFF0000, description=":x: Fant ingen saus :(")
            await ctx.send(content=ctx.message.author.mention, embed=embed)
            await statusmsg.delete()

        os.remove(f"./assets/{ctx.message.author.id}_trace.png")


    @commands.is_owner()
    @commands.command()
    async def tracelimit(self, ctx):
        data = requests.get("https://trace.moe/api/me").json()
        limit = data["limit"]
        limit_ttl = data["limit_ttl"]

        embed = discord.Embed(color=0xE67E22)
        embed.add_field(name="Limits", value=f"{limit} requests\n{limit_ttl} sekunder til resettelse")
        await ctx.send(embed=embed)



def setup(bot):
    bot.add_cog(Whatanime(bot))