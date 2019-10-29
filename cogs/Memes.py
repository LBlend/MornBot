from discord.ext import commands
import discord

from io import BytesIO
from os import remove
from PIL import Image, ImageDraw, ImageFont, ImageOps, ImageFilter
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
            new_f = await self.gen_bilde(self, dorli_tekst, bra_tekst, mem="harald")
            f = discord.File(fp=new_f, filename=f"{ctx.author.id}.png")
            embed = discord.Embed()
            embed.set_image(url=f'attachment://{ctx.author.id}.png')
            await Defaults.set_footer(ctx, embed)
            await ctx.send(embed=embed, file=f)

    @staticmethod
    async def gen_bilde(self, dorli_tekst, bra_tekst, mem):
        font = './assets/fonts/Roboto_Mono/RobotoMono-Medium.ttf'
        top_text, top_font = format_text(dorli_tekst, 505, font)
        bottom_text, bottom_font = format_text(bra_tekst, 505, font)

        image = Image.open(f'./assets/meme_templates/{mem}.png').convert('RGBA')
        color = (0, 0, 0, 255)

        box = Image.new('RGBA', (510, 510), (255, 255, 255, 255))
        draw = ImageDraw.Draw(box)
        font_size = draw.multiline_textsize(top_text, font=top_font)
        font_size = ((box.size[0] - font_size[0]) / 2, (box.size[1] - font_size[1]) / 2)
        draw.multiline_text(font_size, top_text, font=top_font, fill=color, align='center')
        image.paste(box, (514, 0))

        box = Image.new('RGBA', (505, 505), (255, 255, 255, 255))
        draw = ImageDraw.Draw(box)
        draw.multiline_text(font_size, bottom_text, font=bottom_font, fill=color, align='center')
        image.paste(box, (514, 514))

        file = BytesIO()
        image.save(file, format="PNG")
        file.seek(0)
        return file


    """
    Quick fix solution. Improve the command below later
    """
    @commands.bot_has_permissions(embed_links=True, attach_files=True)
    @commands.cooldown(1, 5, commands.BucketType.guild)
    @commands.command(aliases=['kjempenepe'])
    async def nepe(self, ctx, bruker: discord.Member=None):
        """Kjempenepe"""

        async with ctx.channel.typing():

            await bruker.avatar_url_as(format='png').save(fp=f'./assets/temp/{bruker.id}.png')
            avatar = Image.open(f'./assets/temp/{bruker.id}.png')
            nepe = Image.open('./assets/misc/nepe.png')

            mask = Image.open('./assets/misc/nepe_mask.png').convert('L')
            masked_avatar = ImageOps.fit(avatar, mask.size, centering=(0.5, 0.5))
            masked_avatar.putalpha(mask)
            masked_avatar.save(f'./assets/temp/{bruker.id}.png')

            avatar = Image.open(f'./assets/temp/{bruker.id}.png').rotate(30)
            nepe.paste(avatar, (281, 422), avatar)
            nepe.save(f'./assets/temp/{bruker.id}_edit.png')

            f = discord.File(fp=f'./assets/temp/{bruker.id}_edit.png', filename=f"{ctx.author.id}.png")
            embed = discord.Embed()
            embed.set_image(url=f'attachment://{ctx.author.id}.png')
            await Defaults.set_footer(ctx, embed)
            await ctx.send(embed=embed, file=f)

            remove(f'./assets/temp/{bruker.id}.png')
            remove(f'./assets/temp/{bruker.id}_edit.png')


def setup(bot):
    bot.add_cog(Memes(bot))
