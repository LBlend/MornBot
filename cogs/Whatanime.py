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


class Whatanime:
    def __init__(self, bot):
        self.bot = bot


    @commands.cooldown(1, 10, commands.BucketType.guild)
    @commands.command(aliases=["anime", "ani", "source", "saus", "sauce"])
    async def whatanime(self, ctx, bilde=None):
        """Finner ut hvilken anime et skjermbilde er tatt fra"""

        #   Statusmelding
        embed = discord.Embed()
        embed.description = "Finner saus... :mag_right:"
        statusmsg = await ctx.send(embed=embed)

        #   Hent bilde
        if ctx.message.attachments != []:
            await ctx.message.attachments[0].save(fp=f"{ctx.message.author.id}_trace.png")
        else:
            try:
                urllib.request.urlretrieve(str(bilde), f"{ctx.message.author.id}_trace.png")
            except:
                await ctx.send(f"{ctx.message.author.mention} Henting av bilde feilet")
                return

        #   Sjekk størrelse, compression
        filesize = os.path.getsize(f"{ctx.message.author.id}_trace.png")
        if filesize > 1000000:
            basewidth = 300
            img = Image.open(f"{ctx.message.author.id}_trace.png")
            wpercent = (basewidth / float(img.size[0]))
            hsize = int((float(img.size[1]) * float(wpercent)))
            img = img.resize((basewidth, hsize), Image.ANTIALIAS)
            img.save(f"{ctx.message.author.id}_trace.png")

            #   Dobbelsjekk
            newFilesize = os.path.getsize(f"{ctx.message.author.id}_trace.png")
            if newFilesize > 1000000:
                embed = discord.Embed(color=0xF02B30)
                embed.description = ":x: Filen er for stor. Prøv med en mindre fil"
                await statusmsg.edit(embed=embed)
                os.remove(f"{ctx.message.author.id}_trace.png")
                return

        #   POST
        with open(f"{ctx.message.author.id}_trace.png", "rb") as f:
            base = base64.standard_b64encode(f.read())
            data = requests.post("https://trace.moe/api/search", data={'image': base}).json()    

        #   Hent data
        anilistId = data["docs"][0]["anilist_id"]
        malId = data["docs"][0]["mal_id"]
        romajiTitle = data["docs"][0]["title_romaji"]
        nativeTitle = data["docs"][0]["title_native"]
        englishTitle = data["docs"][0]["title_english"]
        episode = data["docs"][0]["episode"]
        time = int(data["docs"][0]["at"])
        similarity = data["docs"][0]["similarity"]

        malData = requests.get(f"https://api.jikan.moe/v3/anime/{malId}/pictures").json()
        thumbnail = malData["pictures"][0]["small"]

        #   Konverter
        similarity_percent = round(similarity * 100, 2)
        formattedTime = timedelta(seconds=time)
        if episode == "":
            episode = "0 (Film)"

        #   Embed
        try:
            embed = discord.Embed(title=romajiTitle, color=0x0085ff, url=f"https://anilist.co/anime/{anilistId}")
            embed.set_thumbnail(url=thumbnail)
            embed.set_author(name=ctx.message.author.name, icon_url=ctx.message.author.avatar_url)
            embed.description = f"{nativeTitle}\n{englishTitle}"
            embed.add_field(name="Episode", value=str(episode))
            embed.add_field(name="Tidspunkt", value=str(formattedTime))
            embed.add_field(name="Likhet %", value=f"{similarity_percent}%")
            embed.add_field(name="Lenker", value=f"[MAL](https://myanimelist.net/anime/{malId}) | [Anilist](https://anilist.co/anime/{anilistId})")

            await statusmsg.edit(embed=embed)

        except:
            embed = discord.Embed(color=0xF02B30)
            embed.description = f":x: Fant ingen saus :("
            await statusmsg.edit(embed=embed)

        #   Cleanup
        os.remove(f"{ctx.message.author.id}_trace.png")


    @commands.is_owner()
    @commands.command()
    async def tracelimit(self, ctx):
        data = requests.get("https://trace.moe/api/me").json()
        limit = data["limit"]
        limit_ttl = data["limit_ttl"]

        await ctx.send(f"{limit} requests\n{limit_ttl} sekunder til resettelse")



def setup(bot):
    bot.add_cog(Whatanime(bot))