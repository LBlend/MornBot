import discord
from discord.ext import commands

from base64 import standard_b64encode
from requests import get, post
import os
from datetime import timedelta
from PIL import Image

from .utils import LBlend_utils, Defaults


class Whatanime(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.bot_has_permissions(embed_links=True)
    @commands.cooldown(1, 10, commands.BucketType.guild)
    @commands.command(aliases=['anime', 'ani', 'source', 'saus', 'sauce'])
    async def whatanime(self, ctx, bilde=None):
        """Finner ut hvilken anime et skjermbilde er tatt fra"""

        embed = discord.Embed(description='Finner saus... :mag_right:')
        await Defaults.set_footer(ctx, embed)
        status_msg = await ctx.send(embed=embed)

        if not await LBlend_utils.download_photo(
                ctx, status_msg,
                link=bilde, max_file_size=8,
                meassurement_type='MB',
                filepath=f'./assets/{ctx.author.id}_trace.png'):
            return

        filesize = os.path.getsize(f'./assets/{ctx.author.id}_trace.png')
        if filesize > 1000000:
            base_width = 300
            img = Image.open(f'./assets/{ctx.author.id}_trace.png')
            width_percent = (base_width / float(img.size[0]))
            height_size = int((float(img.size[1]) * float(width_percent)))
            img = img.resize((base_width, height_size), Image.ANTIALIAS)
            img.save(f'./assets/{ctx.author.id}_trace.png')

            new_file_size = os.path.getsize(
                f'./assets/{ctx.author.id}_trace.png')
            if await LBlend_utils.check_file_too_big(
                    ctx, status_msg,
                    file=new_file_size,
                    max_file_size=1,
                    meassurement_type='MB'):
                return os.remove(f'./assets/{ctx.author.id}_trace.png')

        with open(f'./assets/{ctx.author.id}_trace.png', 'rb') as f:
            base = standard_b64encode(f.read())
            data = post(
                'https://trace.moe/api/search',
                data={'image': base}).json()

        similarity = data['docs'][0]['similarity']
        if similarity < 0.85:
            await Defaults.error_warning_edit(
                ctx, status_msg,
                text='Saus ble funnet, men grunnet ' +
                     'lav likhetsprosent, er det høy sannsynlighet ' +
                     'for at dette ikke er riktig saus')
            return os.remove(f'./assets/{ctx.author.id}_trace.png')

        try:
            anilist_id = data['docs'][0]['anilist_id']
            mal_id = data['docs'][0]['mal_id']
            title_romaji = data['docs'][0]['title_romaji']
            title_native = data['docs'][0]['title_native']
            title_english = data['docs'][0]['title_english']
            episode = data['docs'][0]['episode']
            time = int(data['docs'][0]['at'])
        except KeyError:
            await Defaults.error_fatal_edit(
                ctx, status_msg,
                text='Fant ingen saus')
            return os.remove(f'./assets/{ctx.author.id}_trace.png')

        similarity_percent = round(similarity * 100, 2)
        formatted_time = timedelta(seconds=time)
        if episode is '':
            episode = '0 (Film)'

        thumbnail_data = get(
            f'https://api.jikan.moe/v3/anime/{mal_id}/pictures').json()

        embed = discord.Embed(
            title=title_romaji,
            color=0x0085ff,
            url=f'https://anilist.co/anime/{anilist_id}',
            description=f'{title_native}\n{title_english}')
        embed.set_author(
            name=ctx.author.name, icon_url=ctx.author.avatar_url)
        try:
            thumbnail = thumbnail_data['pictures'][0]['small']
            embed.set_thumbnail(url=thumbnail)
        except KeyError:
            pass
        embed.add_field(name='Episode', value=str(episode))
        embed.add_field(name='Tidspunkt', value=str(formatted_time))
        embed.add_field(name='Likhet %', value=f'{similarity_percent}%')
        embed.add_field(
            name='Lenker',
            value=f'[MAL](https://myanimelist.net/anime/{mal_id}) | ' +
            f'[Anilist](https://anilist.co/anime/{anilist_id})')
        await ctx.send(content=ctx.author.mention, embed=embed)
        await status_msg.delete()

        os.remove(f'./assets/{ctx.author.id}_trace.png')

    @commands.bot_has_permissions(embed_links=True)
    @commands.is_owner()
    @commands.command()
    async def tracelimit(self, ctx):
        data = get('https://trace.moe/api/me').json()
        limit = data['limit']
        limit_ttl = data['limit_ttl']

        embed = discord.Embed(color=0xE67E22)
        embed.add_field(
            name='Limits',
            value=f'{limit} requests\n{limit_ttl} sekunder til resettelse')
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Whatanime(bot))
