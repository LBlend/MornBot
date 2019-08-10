import discord
from discord.ext import commands

from codecs import open
from json import load as json_load
from requests import post
from re import sub

from cogs.utils import Defaults

with open('config.json', 'r', encoding='utf8') as f:
    config = json_load(f)
    prefix = config['prefix']


async def set_profile_color(color):
    colors = {
        'blue': 0x3db4f2,
        'purple': 0xc063ff,
        'pink': 0xFC9DD6,
        'orange': 0xEF881A,
        'red': 0xE13333,
        'green': 0x4CCA51,
        'gray': 0x677B94
    }
    if color in colors:
        color = colors[color]
    else:
        color = color.replace('#', '0x')
        color = int(color, 0)
    return color


async def convert_media_format(media_format):
    media_formats = {
        'TV': 'TV-Serie',
        'TV_SHORT': 'Kort TV-Serie',
        'MOVIE': 'Film',
        'SPECIAL': 'Ekstramateriale',
        'MUSIC': 'Musikk',
        'MANGA': 'Manga',
        'NOVEL': 'Novelle',
        'ONE_SHOT': 'Kort Manga'
    }
    try:
        return media_formats[media_format]
    except KeyError:
        return media_format


async def convert_status(status):
    statuses = {
        'FINISHED': 'Fullført',
        'RELEASING': 'Pågående',
        'NOT_YET_RELEASED': 'Ikke utgitt enda',
        'CANCELLED': 'Kansellert'
    }
    try:
        return statuses[status]
    except KeyError:
        return status


class Anime(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.bot_has_permissions(embed_links=True)
    @commands.cooldown(1, 5, commands.BucketType.guild)
    @commands.group()
    async def anilist(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send_help(ctx.command)

    @anilist.command()
    async def animeprofil(self, ctx, *, bruker: str):
        """Viser animeinformasjon til en Anilist-profil"""

        async with ctx.channel.typing():

            # GraphQL 
            query = """
            query ($name: String) {
                User (name: $name) {
                    name
                    siteUrl
                    updatedAt
                    avatar {
                        large
                    }
                    options {
                        profileColor
                    }
                    stats {
                        watchedTime
                        animeStatusDistribution {
                            amount
                        }
                        animeListScores {
                            meanScore
                        }
                    }
                }
            }
            """
            variables = {
                'name': bruker
            }
            try:
                data = post(
                    'https://graphql.anilist.co',
                    json={'query': query, 'variables': variables}).json()
                data = data['data']['User']
                url = data['siteUrl']
            except TypeError:
                return await Defaults.error_fatal_send(
                    ctx, text='Kunne ikke finne brukeren\n\n' +
                        f'Skriv `{prefix}help {ctx.command}` for hjelp',
                        mention=False)

            user_name = data['name']
            profile_pic = data['avatar']['large']
            days_watched = round(data['stats']['watchedTime'] / 1440, 1)
            watching = data['stats']['animeStatusDistribution'][0]['amount']
            planning = data['stats']['animeStatusDistribution'][1]['amount']
            completed = data['stats']['animeStatusDistribution'][2]['amount']
            dropped = data['stats']['animeStatusDistribution'][3]['amount']

            try:
                anime_mean_score = data['stats']['animeListScores']['meanScore']
            except TypeError:
                anime_mean_score = '**Ingen**'
            if not anime_mean_score:
                anime_mean_score = '**Ingen**'

            color = data['options']['profileColor']
            color = await set_profile_color(color)

            embed = discord.Embed(title=user_name, color=color, url=url)
            embed.set_author(name='Anilist', icon_url='https://avatars3.githubusercontent.com/u/18018524?s=200&v=4')
            embed.set_thumbnail(url=profile_pic)
            embed.add_field(name='Gj.snittlig vurdering', value=anime_mean_score)
            embed.add_field(name='Antall dager sett', value=days_watched)
            embed.add_field(name='Antall animer sett', value=completed)
            embed.add_field(name='Ser på nå', value=watching)
            embed.add_field(name='Planlegger å se', value=planning)
            embed.add_field(name='Droppet', value=dropped)
            await Defaults.set_footer(ctx, embed)
            await ctx.send(embed=embed)

    @anilist.command()
    async def mangaprofil(self, ctx, *, bruker: str):
        """Viser mnagainformasjonen til en Anilist-profil"""

        async with ctx.channel.typing():

            # GraphQL 
            query = """
            query ($name: String) {
                User (name: $name) {
                    name
                    siteUrl
                    updatedAt
                    avatar {
                        large
                    }
                    options {
                        profileColor
                    }
                    stats {
                        chaptersRead
                        mangaStatusDistribution {
                            amount
                        }
                        mangaListScores {
                            meanScore
                        }
                    }
                }
            }
            """
            variables = {
                'name': bruker
            }

            try:
                data = post(
                    'https://graphql.anilist.co',
                    json={'query': query, 'variables': variables}).json()
                data = data['data']['User']
                url = data['siteUrl']
            except TypeError:
                return await Defaults.error_fatal_send(
                    ctx, text='Kunne ikke finne brukeren\n\n' +
                        f'Skriv `{prefix}help {ctx.command}` for hjelp')

            user_name = data['name']
            profile_pic = data['avatar']['large']
            chapters_read = data['stats']['chaptersRead']
            reading = data['stats']['mangaStatusDistribution'][0]['amount']
            planning = data['stats']['mangaStatusDistribution'][1]['amount']
            completed = data['stats']['mangaStatusDistribution'][2]['amount']
            dropped = data['stats']['mangaStatusDistribution'][3]['amount']

            try:
                manga_mean_score = data['stats']['mangaListScores']['meanScore']
            except TypeError:
                manga_mean_score = '**Ingen**'
            if not manga_mean_score:
                manga_mean_score = '**Ingen**'

            color = data['options']['profileColor']
            color = await set_profile_color(color)

            embed = discord.Embed(title=user_name, color=color, url=url)
            embed.set_author(name='Anilist', icon_url='https://avatars3.githubusercontent.com/u/18018524?s=200&v=4')
            embed.set_thumbnail(url=profile_pic)
            embed.add_field(name='Gj.snittlig vurdering', value=manga_mean_score)
            embed.add_field(name='Antall kapitler lest', value=chapters_read)
            embed.add_field(name='Antall manga lest', value=completed)
            embed.add_field(name='Leser nå', value=reading)
            embed.add_field(name='Planlegger å lese', value=planning)
            embed.add_field(name='Droppet', value=dropped)
            await Defaults.set_footer(ctx, embed)
            await ctx.send(embed=embed)

    @commands.bot_has_permissions(embed_links=True)
    @commands.cooldown(1, 5, commands.BucketType.guild)
    @commands.command()
    async def anime(self, ctx, *, animenavn: str):
        """Viser informasjon om en anime"""

        async with ctx.channel.typing():

            query = '''
            query ($search: String, $isMain: Boolean) {
                Media (search: $search, type: ANIME) {
                    siteUrl
                    format
                    status
                    description
                    episodes
                    duration
                    genres
                    isAdult
                    bannerImage
                    meanScore
                    coverImage {
                        large
                    }
                    startDate {
                        year
                        month
                        day
                    }
                    endDate {
                        year
                        month
                        day
                    }
                    title {
                        romaji
                        english
                        native
                    }
                    studios(isMain: $isMain) {
                        nodes {
                            name
                            siteUrl
                        }
                    }
                    staff(sort: ROLE) {
                        edges {
                            role
                            node {
                                siteUrl
                                name {
                                    first
                                    last
                                    native
                                }
                            }
                        }
                    }
                }
            }
            '''
            variables = {
                'search': animenavn,
                'isMain': True
            }
            try:
                data = post('https://graphql.anilist.co', json={'query': query, 'variables': variables}).json()
                data = data['data']['Media']
                url = data['siteUrl']
            except TypeError:
                return await Defaults.error_fatal_send(
                    ctx, text='Kunne ikke finne animen\n\n' +
                              f'Skriv `{prefix}help {ctx.command}` for hjelp',
                    mention=False)

            nsfw = data['isAdult']
            if nsfw:
                return await Defaults.error_fatal_send(ctx, text='Animen du søkte på er NSFW. ' +
                                                                 'Gjør kommandoen i en NSFW-kanal isteden')

            cover_image = data['coverImage']['large']
            banner_image = data['bannerImage']
            mean_score = data['meanScore']

            title_romaji = data['title']['romaji']
            title_native = data['title']['native']
            title_english = data['title']['english']
            titles = [title_romaji, title_native, title_english]
            for i, title in enumerate(titles):
                if title is None:
                    titles[i] = ''
            title_romaji, title_native, title_english = titles

            description = sub(r'<.*?>', '', data['description'])
            genres = ', '.join(data['genres'])

            studios = data['studios']['nodes']
            studios_string = ''
            for studio in studios:
                studio_name = studio['name']
                studio_url = studio['siteUrl']
                studios_string += f'[{studio_name}]({studio_url})\n'

            staff = data['staff']['edges']
            director_string = ''
            for staff_member in staff:
                if staff_member['role'] == 'Director':
                    director_first_name = staff_member['node']['name']['first']
                    director_last_name = staff_member['node']['name']['last']
                    director_native_name = staff_member['node']['name']['native']
                    director_url = staff_member['node']['siteUrl']
                    director_string += f'[{director_first_name} {director_last_name} ' +\
                                       f'({director_native_name})]({director_url})'

            episodes = data['episodes']
            duration = data['duration']

            release_day = data['startDate']['day']
            release_month = data['startDate']['month']
            release_year = data['startDate']['year']
            end_day = data['endDate']['day']
            end_month = data['endDate']['month']
            end_year = data['endDate']['year']

            numbers = [episodes, duration, release_day, release_month, release_year, end_day, end_month, end_year]
            for i, number in enumerate(numbers):
                if number is None:
                    numbers[i] = '?'
            episodes, duration, release_day, release_month, release_year, end_day, end_month, end_year = numbers
            length_string = ''
            if duration == 1:
                length_string += 'minutt '
            else:
                length_string += 'minutter '
            if episodes == 1:
                length_string += 'lang'
            else:
                length_string += 'lange'

            release_date = f'{release_day}.{release_month}.{release_year}'
            end_date = f'{end_day}.{end_month}.{end_year}'
            if release_date == end_date:
                date = release_date
            else:
                date = f'{release_date} - {end_date}'

            status = data['status']
            status = await convert_status(status)

            media_format = data['format']
            media_format = await convert_media_format(media_format)

            embed = discord.Embed(color=0x02A9FF, title=title_romaji, url=url,
                                  description=f'{title_native}\n{title_english}')
            embed.set_thumbnail(url=cover_image)
            embed.add_field(name='Format', value=media_format)
            embed.add_field(name='Status', value=status)
            if studios_string:
                embed.add_field(name='Studio', value=studios_string)
            if director_string:
                embed.add_field(name='Regissør', value=director_string)
            embed.add_field(name='Utgivelsesdato', value=date)
            if media_format == 'Film':
                embed.add_field(name='Lengde', value=f'{duration} minutter')
            else:
                embed.add_field(name='Episoder', value=f'{episodes} ({duration} {length_string})')
            if mean_score:
                embed.add_field(name='Gj.snittsvurdering', value=f'{mean_score}/100')
            embed.add_field(name='Sjangere', value=genres)
            if len(description) < 1024:
                embed.add_field(name='Sammendrag', value=description, inline=False)
            if banner_image:
                embed.set_image(url=banner_image)
            await Defaults.set_footer(ctx, embed)
            await ctx.send(embed=embed)

    @commands.bot_has_permissions(embed_links=True)
    @commands.cooldown(1, 5, commands.BucketType.guild)
    @commands.command()
    async def manga(self, ctx, *, manganavn: str):
        """Viser informasjon om en anime"""

        async with ctx.channel.typing():

            query = '''
                query ($search: String) {
                    Media (search: $search, type: MANGA) {
                        siteUrl
                        format
                        status
                        description
                        volumes
                        chapters
                        genres
                        isAdult
                        bannerImage
                        meanScore
                        coverImage {
                            large
                        }
                        startDate {
                            year
                            month
                            day
                        }
                        endDate {
                            year
                            month
                            day
                        }
                        title {
                            romaji
                            english
                            native
                        }
                        staff(sort: ROLE) {
                            edges {
                                role
                                node {
                                    siteUrl
                                    name {
                                        first
                                        last
                                        native
                                    }
                                }
                            }
                        }
                    }
                }
                '''
            variables = {
                'search': manganavn
            }
            try:
                data = post('https://graphql.anilist.co', json={'query': query, 'variables': variables}).json()
                data = data['data']['Media']
                url = data['siteUrl']
            except TypeError:
                return await Defaults.error_fatal_send(
                    ctx, text='Kunne ikke finne mangaen\n\n' +
                              f'Skriv `{prefix}help {ctx.command}` for hjelp',
                    mention=False)

            nsfw = data['isAdult']
            if nsfw:
                return await Defaults.error_fatal_send(ctx, text='Mangaen du søkte på er NSFW. ' +
                                                                 'Gjør kommandoen i en NSFW-kanal isteden')

            cover_image = data['coverImage']['large']
            banner_image = data['bannerImage']
            mean_score = data['meanScore']

            title_romaji = data['title']['romaji']
            title_native = data['title']['native']
            title_english = data['title']['english']
            titles = [title_romaji, title_native, title_english]
            for i, title in enumerate(titles):
                if title is None:
                    titles[i] = ''
            title_romaji, title_native, title_english = titles

            description = sub(r'<.*?>', '', data['description'])
            genres = ', '.join(data['genres'])

            staff = data['staff']['edges']
            staff_string = ''
            for staff_member in staff:
                staff_first_name = staff_member['node']['name']['first']
                staff_last_name = staff_member['node']['name']['last']
                staff_native_name = staff_member['node']['name']['native']
                staff_url = staff_member['node']['siteUrl']
                staff_string += f'[{staff_first_name} {staff_last_name} ({staff_native_name})]({staff_url})\n'

            chapters = data['chapters']
            volumes = data['volumes']

            release_day = data['startDate']['day']
            release_month = data['startDate']['month']
            release_year = data['startDate']['year']

            numbers = [chapters, volumes, release_day, release_month, release_year]
            for i, number in enumerate(numbers):
                if number is None:
                    numbers[i] = '?'
            chapters, volumes, release_day, release_month, release_year = numbers
            release_date = f'{release_day}.{release_month}.{release_year}'

            chapters_string = ''
            if chapters == 1:
                chapters_string += 'kapittel'
            else:
                chapters_string += 'kapitler'

            status = data['status']
            status = await convert_status(status)

            media_format = data['format']
            media_format = await convert_media_format(media_format)

            embed = discord.Embed(color=0x02A9FF, title=title_romaji, url=url,
                                  description=f'{title_native}\n{title_english}')
            embed.set_thumbnail(url=cover_image)
            embed.add_field(name='Format', value=media_format)
            embed.add_field(name='Status', value=status)
            if staff_string:
                embed.add_field(name='Laget av', value=staff_string)
            embed.add_field(name='Utgivelsesdato', value=release_date)
            embed.add_field(name='Lengde', value=f'{chapters} {chapters_string}\n{volumes} volum')
            if mean_score:
                embed.add_field(name='Gj.snittsvurdering', value=f'{mean_score}/100')
            embed.add_field(name='Sjangere', value=genres)
            if len(description) < 1024:
                embed.add_field(name='Sammendrag', value=description, inline=False)
            if banner_image:
                embed.set_image(url=banner_image)
            await Defaults.set_footer(ctx, embed)
            await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Anime(bot))
