import discord
from discord.ext import commands

from os import remove
from PIL import Image, ImageOps, ImageEnhance

from .utils import Defaults, LBlend_utils


class ImageManipulation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.bot_has_permissions(embed_links=True, attach_files=True)
    @commands.cooldown(1, 5, commands.BucketType.guild)
    @commands.command()
    async def pride(self, ctx, *, bruker: discord.Member=None):
        """Pride"""

        if not bruker:
            bruker = ctx.author

        async with ctx.channel.typing():
            await bruker.avatar_url_as(format='png').save(fp=f'./assets/{bruker.id}_raw.png')

            raw_image = Image.open(f'./assets/{bruker.id}_raw.png')
            image_edit = raw_image.convert('RGBA')
            width, height = image_edit.size
            gay = Image.open('./assets/gay.png')
            gay_edit = gay.convert('RGBA')
            gay_edit = gay_edit.resize((width, height), Image.ANTIALIAS)
            gay_edit.save(f'./assets/gay.png')
            mask = Image.open(f'./assets/gay.png', 'r')
            image_edit.paste(gay_edit, mask=mask)
            image_edit.save(f'./assets/{bruker.id}_edit.png')

            f = discord.File(f'./assets/{bruker.id}_edit.png')
            embed = discord.Embed()
            embed.set_image(url=f'attachment://{bruker.id}_edit.png')
            await Defaults.set_footer(ctx, embed)
            await ctx.send(embed=embed, file=f)

            try:
                remove(f'./assets/{bruker.id}_raw.png')
                remove(f'./assets/{bruker.id}_edit.png')
            except:
                pass

            return

    @commands.bot_has_permissions(embed_links=True, attach_files=True)
    @commands.cooldown(1, 5, commands.BucketType.guild)
    @commands.command(aliases=['needsmorejpeg', 'jpg', 'jpeg'])
    async def needsmorejpg(self, ctx, bilde=None):
        """JPG er et kjempebra bildeformat"""

        async with ctx.channel.typing():

            if not await LBlend_utils.download_photo(
                    ctx, link=bilde, max_file_size=8, meassurement_type='MB',
                    filepath=f'./assets/{ctx.author.id}_raw.png'):
                return

            raw_image = Image.open(f'./assets/{ctx.author.id}_raw.png')
            image_edit = raw_image.convert('RGB')
            image_edit.save(
                f'./assets/{ctx.author.id}_edit.jpg', quality=5)

            f = discord.File(f'./assets/{ctx.author.id}_edit.jpg')
            embed = discord.Embed(color=ctx.me.color)
            embed.set_image(url=f'attachment://{ctx.author.id}_edit.jpg')
            await Defaults.set_footer(ctx, embed)
            await ctx.send(embed=embed, file=f)

            try:
                remove(f'./assets/{ctx.author.id}_raw.png')
                remove(f'./assets/{ctx.author.id}_edit.jpg')
            except:
                pass

            return

    @commands.bot_has_permissions(embed_links=True, attach_files=True)
    @commands.cooldown(1, 5, commands.BucketType.guild)
    @commands.command(aliases=['invert'])
    async def inverter(self, ctx, bilde=None):
        """Inverterer fargene i bildet"""

        async with ctx.channel.typing():

            if not await LBlend_utils.download_photo(
                    ctx, link=bilde, max_file_size=8, meassurement_type='MB',
                    filepath=f'./assets/{ctx.author.id}_raw.png'):
                return

            raw_image = Image.open(f'./assets/{ctx.author.id}_raw.png')
            image_edit = raw_image.convert('RGB')
            image_edit = ImageOps.invert(image_edit)
            image_edit.save(f'./assets/{ctx.author.id}_edit.png')

            f = discord.File(f'./assets/{ctx.author.id}_edit.png')
            embed = discord.Embed(color=ctx.me.color)
            embed.set_image(url=f'attachment://{ctx.author.id}_edit.png')
            await Defaults.set_footer(ctx, embed)
            await ctx.send(embed=embed, file=f)

            try:
                remove(f'./assets/{ctx.author.id}_raw.png')
                remove(f'./assets/{ctx.author.id}_edit.png')
            except:
                pass

            return

    @commands.bot_has_permissions(embed_links=True, attach_files=True)
    @commands.cooldown(1, 5, commands.BucketType.guild)
    @commands.command(aliases=['flip', 'mirror'])
    async def flipp(self, ctx, bilde=None):
        """Snur bildet"""

        async with ctx.channel.typing():

            if not await LBlend_utils.download_photo(
                    ctx, link=bilde, max_file_size=8, meassurement_type='MB',
                    filepath=f'./assets/{ctx.author.id}_raw.png'):
                return

            raw_image = Image.open(f'./assets/{ctx.author.id}_raw.png')
            image_edit = raw_image.convert('RGBA')
            image_edit = image_edit.rotate(180)
            image_edit.save(f'./assets/{ctx.author.id}_edit.png')

            f = discord.File(f'./assets/{ctx.author.id}_edit.png')
            embed = discord.Embed(color=ctx.me.color)
            embed.set_image(url=f'attachment://{ctx.author.id}_edit.png')
            await Defaults.set_footer(ctx, embed)
            await ctx.send(embed=embed, file=f)

            try:
                remove(f'./assets/{ctx.author.id}_raw.png')
                remove(f'./assets/{ctx.author.id}_edit.png')
            except:
                pass

            return

    @commands.bot_has_permissions(embed_links=True, attach_files=True)
    @commands.cooldown(1, 5, commands.BucketType.guild)
    @commands.command(
        aliases=['svarthvitt', 'svart-hvitt', 'grayscale', 'greyscale'])
    async def grå(self, ctx, bilde=None):
        """Gjør bildet svart-hvitt"""

        async with ctx.channel.typing():

            if not await LBlend_utils.download_photo(
                    ctx, link=bilde, max_file_size=8, meassurement_type='MB',
                    filepath=f'./assets/{ctx.author.id}_raw.png'):
                return

            raw_image = Image.open(f'./assets/{ctx.author.id}_raw.png')
            image_edit = raw_image.convert('RGBA')
            image_edit = ImageOps.grayscale(image_edit)
            image_edit.save(f'./assets/{ctx.author.id}_edit.png')

            f = discord.File(f'./assets/{ctx.author.id}_edit.png')
            embed = discord.Embed(color=ctx.me.color)
            embed.set_image(url=f'attachment://{ctx.author.id}_edit.png')
            await Defaults.set_footer(ctx, embed)
            await ctx.send(embed=embed, file=f)

            try:
                remove(f'./assets/{ctx.author.id}_raw.png')
                remove(f'./assets/{ctx.author.id}_edit.png')
            except:
                pass

            return

    @commands.bot_has_permissions(embed_links=True, attach_files=True)
    @commands.cooldown(1, 5, commands.BucketType.guild)
    @commands.command(aliases=['friter', 'fry'])
    async def deepfry(self, ctx, bilde=None):
        """Voldtar bildet med litt god gammaldags fritering"""

        async with ctx.channel.typing():

            if not await LBlend_utils.download_photo(
                    ctx, link=bilde, max_file_size=8, meassurement_type='MB',
                    filepath=f'./assets/{ctx.author.id}_raw.jpg'):
                return

            raw_image = Image.open(f'./assets/{ctx.author.id}_raw.jpg')
            image_edit = raw_image.convert('RGB')
            image_edit = ImageOps.posterize(image_edit, bits=1)
            image_edit = ImageEnhance.Sharpness(image_edit)
            image_edit = image_edit.enhance(3)
            image_edit = ImageEnhance.Contrast(image_edit)
            image_edit = image_edit.enhance(1.5)
            image_edit = ImageEnhance.Brightness(image_edit)
            image_edit = image_edit.enhance(1.5)
            image_edit = ImageEnhance.Color(image_edit)
            image_edit = image_edit.enhance(1.5)
            image_edit.save(f'./assets/{ctx.author.id}_edit.png')

            f = discord.File(f'./assets/{ctx.author.id}_edit.png')
            embed = discord.Embed(color=ctx.me.color)
            embed.set_image(url=f'attachment://{ctx.author.id}_edit.png')
            await Defaults.set_footer(ctx, embed)
            await ctx.send(embed=embed, file=f)

            try:
                remove(f'./assets/{ctx.author.id}_raw.jpg')
                remove(f'./assets/{ctx.author.id}_edit.png')
            except:
                pass

            return


def setup(bot):
    bot.add_cog(ImageManipulation(bot))
