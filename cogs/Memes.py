from discord.ext import commands
import discord

from io import BytesIO
from os import remove
from PIL import Image, ImageDraw, ImageFont
import textwrap

from cogs.utils import Defaults


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
            new_f = await self.gen_bilde(self, dorli_tekst, bra_tekst, mem="desanti")
            f = discord.File(fp=new_f, filename=f"{ctx.author.id}.png")
            embed = discord.Embed()
            embed.set_image(url=f'attachment://{ctx.author.id}.png')
            await Defaults.set_footer(ctx, embed)
            await ctx.send(embed=embed, file=f)

    @commands.bot_has_permissions(embed_links=True, attach_files=True)
    @commands.cooldown(1, 5, commands.BucketType.guild)
    @commands.command()
    async def egon(self, ctx, dorli_tekst: str, bra_tekst: str):
        """Egon mem"""

        async with ctx.channel.typing():
            new_f = await self.gen_bilde(self, dorli_tekst, bra_tekst, mem="egon")
            f = discord.File(fp=new_f, filename=f"{ctx.author.id}.png")
            embed = discord.Embed()
            embed.set_image(url=f'attachment://{ctx.author.id}.png')
            await Defaults.set_footer(ctx, embed)
            await ctx.send(embed=embed, file=f)

    @commands.bot_has_permissions(embed_links=True, attach_files=True)
    @commands.cooldown(1, 5, commands.BucketType.guild)
    @commands.command(aliases=['konge'])
    async def harald(self, ctx, dorli_tekst: str, bra_tekst: str):
        """Harald mem"""

        async with ctx.channel.typing():
            new_f = await self.gen_bilde(self, dorli_tekst, bra_tekst, mem="desanti")
            f = discord.File(fp=new_f, filename=f"{ctx.author.id}.png")
            embed = discord.Embed()
            embed.set_image(url=f'attachment://{ctx.author.id}.png')
            await Defaults.set_footer(ctx, embed)
            await ctx.send(embed=embed, file=f)

    @staticmethod
    async def gen_bilde(self, dorli_tekst, bra_tekst, mem):
        font = './assets/fonts/Roboto_Mono/RobotoMono-Medium.ttf'
        top_text, top_font = format_text(dorli_tekst, 800, font)
        bottom_text, bottom_font = format_text(bra_tekst, 800, font)

        image = Image.open(f'./assets/meme_templates/{mem}.png').convert('RGBA')
        color = (0, 0, 0, 255)

        box = Image.new('RGBA', (505, 505), (255, 255, 255, 255))
        draw = ImageDraw.Draw(box)
        font_size = draw.multiline_textsize(top_text, font=top_font)
        font_size = ((box.size[0] - font_size[0]) / 2, (box.size[1] - font_size[1]) / 2)
        draw.multiline_text(font_size, top_text, font=top_font, fill=color, align='center')
        image.paste(box, (519, 4))

        box = Image.new('RGBA', (505, 505), (255, 255, 255, 255))
        draw = ImageDraw.Draw(box)
        draw.multiline_text(font_size, bottom_text, font=bottom_font, fill=color, align='center')
        image.paste(box, (519, 517))

        file = BytesIO()
        image.save(file, format="PNG")
        file.seek(0)
        return file


def setup(bot):
    bot.add_cog(Memes(bot))
