import discord
import asyncio
from discord.ext import commands

from os import path
from PIL import Image
import numpy as np
from wordcloud import WordCloud


class Ordsky:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["wordcloud", "wc", "sky"])
    async def ordsky(self, ctx, maskevalg=None, bruker: discord.Member=None):
        """Generer en ordsky"""

        if not bruker:
            bruker = ctx.message.author

        statusmsg = await ctx.send("Teller ord...")

        with open(f"./assets/ordsky/tekst/{bruker.id}.txt", "w+") as f:
            for channel in ctx.message.guild.text_channels:
                async for message in channel.history(limit=1500):
                    if message.author.id == bruker.id:
                        try:
                            f.write(f"{message.content} ")
                        except:
                            pass
                    else:
                        pass

        await statusmsg.edit(content="Genererer ordsky...")
        
        #   Maskevalg
        if maskevalg == "ostehøvel":
            maskbilde = np.array(Image.open(path.join("./assets/ordsky/mask/", "ostmask.png")))
        else:
            maskbilde = np.array(Image.open(path.join("./assets/ordsky/mask/", "owomask.png")))

        #   Åpne ordtekstfil
        text = open(path.join("./assets/ordsky/tekst/", f"{bruker.id}.txt")).read()

        #   Ordsky innstillinger
        wc = WordCloud(font_path=None, max_words=2000, mask=maskbilde)

        #   Generer ordsky
        wc.generate(text)

        #   Frequencies
        #wc.generate_from_frequencies(test, max_font_size=96)

        #   Lagre bilde
        wc.to_file(f"./assets/ordsky/bilde/{bruker.id}.png")

        #   Send bilde
        await ctx.send(f"Generert ordsky for <@{bruker.id}>", file=discord.File(f"./assets/ordsky/bilde/{bruker.id}.png"))

        await statusmsg.delete()


def setup(bot):
    bot.add_cog(Ordsky(bot))