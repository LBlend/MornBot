import discord
from discord.ext import commands

from os import remove
from PIL import Image

from .utils import LBlend_utils


class ImageManipulation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.bot_has_permissions(embed_links=True, attach_files=True)
    @commands.cooldown(1, 5, commands.BucketType.guild)
    @commands.command(aliases=['needsmorejpeg', 'jpg', 'jpeg'])
    async def needsmorejpg(self, ctx, bilde=None):

        embed = discord.Embed(description='JPG-ifiserer...')
        embed.set_footer(
            icon_url=ctx.author.avatar_url,
            text=f'{ctx.author.name}#{ctx.author.discriminator}')
        status_msg = await ctx.send(embed=embed)

        if not await LBlend_utils.download_photo(
                ctx, status_msg,
                link=bilde, max_file_size=8,
                meassurement_type='MB',
                filepath=f'./assets/{ctx.author.id}_notjpged.png'):
            return

        raw_image = Image.open(f'./assets/{ctx.author.id}_notjpged.png')
        raw_image_not_rgb = raw_image.convert('RGB')
        raw_image_not_rgb.save(
            f'./assets/{ctx.author.id}_jpged.jpg', quality=5)

        f = discord.File(f'./assets/{ctx.author.id}_jpged.jpg')
        await ctx.send(file=f)
        await status_msg.delete()

        try:
            remove(f'./assets/{ctx.author.id}_notjpged.png')
            remove(f'./assets/{ctx.author.id}_jpged.jpg')
        except:
            pass


def setup(bot):
    bot.add_cog(ImageManipulation(bot))
