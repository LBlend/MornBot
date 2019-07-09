from discord.ext import commands
import discord

from os import remove
from PIL import Image, ImageDraw, ImageFont
import textwrap

from requests import get
import shutil
import functools

from cogs.utils import Defaults, LBlend_utils


def format_text(text, textbox_width, font_ttf):
    font_size = int(textbox_width/(3*len(text)**(1/2)))
    font = ImageFont.truetype(font_ttf, font_size)

    line_length = int(textbox_width/font_size)
    text = textwrap.fill(text, width=line_length)

    return text, font


class Memes(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.bot_has_permissions(embed_links=True, attach_files=True)
    @commands.cooldown(1, 5, commands.BucketType.guild)
    @commands.command(aliases=['santi'])
    async def desanti(self, ctx, dorli_tekst: str, bra_tekst: str):
        """Desanti mem"""

        async with ctx.channel.typing():
            
            font = './assets/fonts/Roboto_Mono/RobotoMono-Medium.ttf'
            top_text, top_font = format_text(dorli_tekst, 1000, font)
            bottom_text, bottom_font = format_text(bra_tekst, 1000, font)

            image = Image.open(f'./assets/desanti.png').convert('RGBA')
            color = (0, 0, 0, 255)

            top = Image.new('RGBA', (638, 688), (255, 255, 255, 255))
            draw = ImageDraw.Draw(top)
            font_size = draw.multiline_textsize(top_text, font=top_font)
            font_size = ((top.size[0] - font_size[0]) / 2, (top.size[1] - font_size[1]) / 2)
            draw.multiline_text(font_size, top_text, font=top_font, fill=color, align='center')
            image.paste(top, (655, 6))

            bottom = Image.new('RGBA', (640, 770), (255, 255, 255, 255))
            draw = ImageDraw.Draw(bottom)
            font_size = draw.multiline_textsize(bottom_text, font=bottom_font)
            font_size = ((bottom.size[0] - font_size[0]) / 2, (bottom.size[1] - font_size[1]) / 2)
            draw.multiline_text(font_size, bottom_text, font=bottom_font, fill=color, align='center')
            image.paste(bottom, (654, 701))

            image.save(f'./assets/{ctx.author.id}_edit.png')

            f = discord.File(f'./assets/{ctx.author.id}_edit.png')
            embed = discord.Embed()
            embed.set_image(url=f'attachment://{ctx.author.id}_edit.png')
            await Defaults.set_footer(ctx, embed)
            await ctx.send(embed=embed, file=f)

            try:
                remove(f'./assets/{ctx.author.id}_raw.png')
                remove(f'./assets/{ctx.author.id}_edit.png')
            except:
                pass


def setup(bot):
    bot.add_cog(Memes(bot))
