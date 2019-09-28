from discord.ext import commands
import discord

from requests import post

from cogs.utils import Defaults


async def set_color(color):
    """Converts anilist colors to hext"""

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
    """Formats media format names"""

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
    """Formats status names"""

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
        """Se informasjon om noe fra Anilist"""

        if ctx.invoked_subcommand is None:
            await ctx.send_help(ctx.command)

    @anilist.command(aliases=['anime'])
    async def animestats(self, ctx, *, bruker: str):
        """Viser animeinformasjon til en Anilist-profil"""

        async with ctx.channel.typing():

            # GraphQL 
            query = """
            query ($name: String) {
                User(name: $name) {
                    name
                    siteUrl
                    updatedAt
                    avatar {
                        large
                    }
                    options {
                        profileColor
                    }
                    statistics {
                        anime {
                            minutesWatched
                            episodesWatched
                            meanScore
                            statuses {
                                count
                                status
                                minutesWatched
                            }
                            studios(limit: 3, sort: COUNT_DESC) {
                                studio {
                                    name
                                    siteUrl
                                }
                            }
                            genres(limit: 3, sort: COUNT_DESC) {
                                genre
                            }
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
                              f'Skriv `{self.bot.prefix}help {ctx.command}` for hjelp')

            user_name = data['name']
            profile_pic = data['avatar']['large']
            days_watched = round(data['statistics']['anime']['minutesWatched'] / 1440, 1)
            episodes_watched = data['statistics']['anime']['episodesWatched']
            color = data['options']['profileColor']
            color = await set_color(color)
            
            statuses = {}
            for status in data['statistics']['anime']['statuses']:
                status_name = status['status']
                status_count = status['count']
                status_minutes = status['minutesWatched']
                statuses.update({f'{status_name}': {'count': status_count, 'minutes': status_minutes}})

            try:
                completed = statuses['COMPLETED']['count']
            except KeyError:
                completed = 0
            try:
                watching = statuses['CURRENT']['count']
            except KeyError:
                watching = 0
            try:
                planning = statuses['PLANNING']['count']
                planning_days = round(statuses['PLANNING']['minutes'] / 1440, 1)
            except KeyError:
                planning = 0
                planning_days = 0
            try:
                dropped = statuses['DROPPED']['count']
            except KeyError:
                dropped = 0
            
            anime_mean_score = data['statistics']['anime']['meanScore']
            if anime_mean_score == 0:
                anime_mean_score = '**Ingen**'

            genres = []
            for genre in data['statistics']['anime']['genres']:
                genres.append(genre['genre'])
            most_watched_genres = ', '.join(genres)

            studios = []
            for studio in data['statistics']['anime']['studios']:
                studio_name = studio['studio']['name']
                studio_url = studio['studio']['siteUrl']
                studios.append(f'[{studio_name}]({studio_url})')
            most_watched_studios = ' | '.join(studios)

            embed = discord.Embed(title=user_name, color=color, url=url)
            embed.set_author(name='Anilist', icon_url='https://anilist.co/img/logo_al.png')
            embed.set_thumbnail(url=profile_pic)
            embed.add_field(name='Gj.snittsvurdering gitt', value=anime_mean_score)
            embed.add_field(name='Antall dager sett', value=days_watched)
            embed.add_field(name='Antall episoder sett', value=episodes_watched)
            embed.add_field(name='Antall animer sett', value=completed)
            embed.add_field(name='Ser på nå', value=watching)
            embed.add_field(name='Planlegger å se', value=f'{planning}\n({planning_days} dager)')
            embed.add_field(name='Droppet', value=dropped)
            if most_watched_genres is not '':
                embed.add_field(name='Mest sette sjangere', value=most_watched_genres, inline=False)
            if most_watched_studios is not '':
                embed.add_field(name='Mest sette studioer', value=most_watched_studios, inline=False)
            await Defaults.set_footer(ctx, embed)
            await ctx.send(embed=embed)

    @anilist.command(aliases=['manga'])
    async def mangastats(self, ctx, *, bruker: str):
        """Viser mnagainformasjonen til en Anilist-profil"""

        async with ctx.channel.typing():

            # GraphQL 
            query = """
            query ($name: String) {
                User(name: $name) {
                    name
                    siteUrl
                    updatedAt
                    avatar {
                        large
                    }
                    options {
                        profileColor
                    }
                    statistics {
                        manga {
                            chaptersRead
                            volumesRead
                            meanScore
                            statuses {
                                count
                                status
                                chaptersRead
                            }
                            staff(limit: 3, sort: COUNT_DESC) {
                                staff {
                                    name {
                                        full
                                        native
                                    }
                                    siteUrl
                                }
                            }
                            genres(limit: 3, sort: COUNT_DESC) {
                                genre
                            }
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
                              f'Skriv `{self.bot.prefix}help {ctx.command}` for hjelp')

            user_name = data['name']
            profile_pic = data['avatar']['large']
            chapters_read = round(data['statistics']['manga']['chaptersRead'] / 1440, 1)
            volumes_read = data['statistics']['manga']['volumesRead']
            color = data['options']['profileColor']
            color = await set_color(color)
            
            statuses = {}
            for status in data['statistics']['manga']['statuses']:
                status_name = status['status']
                status_count = status['count']
                status_minutes = status['chaptersRead']
                statuses.update({f'{status_name}': {'count': status_count, 'minutes': status_minutes}})

            try:
                completed = statuses['COMPLETED']['count']
            except KeyError:
                completed = 0
            try:
                reading = statuses['CURRENT']['count']
            except KeyError:
                reading = 0
            try:
                planning = statuses['PLANNING']['count']
                planning_days = statuses['PLANNING']['chaptersRead']
            except KeyError:
                planning = 0
                planning_days = 0
            try:
                dropped = statuses['DROPPED']['count']
            except KeyError:
                dropped = 0
            
            manga_mean_score = data['statistics']['manga']['meanScore']
            if manga_mean_score == 0:
                manga_mean_score = '**Ingen**'

            genres = []
            for genre in data['statistics']['manga']['genres']:
                genres.append(genre['genre'])
            most_read_genres = ', '.join(genres)

            staff = []
            for staffmember in data['statistics']['manga']['staff']:
                staff_name = staffmember['staff']['name']['full'] + ' (' + staffmember['staff']['name']['native'] + ')'
                staff_url = staffmember['staff']['siteUrl']
                staff.append(f'[{staff_name}]({staff_url})')
            most_read_staff = ' | '.join(staff)

            embed = discord.Embed(title=user_name, color=color, url=url)
            embed.set_author(name='Anilist', icon_url='https://anilist.co/img/logo_al.png')
            embed.set_thumbnail(url=profile_pic)
            embed.add_field(name='Gj.snittsvurdering gitt', value=manga_mean_score)
            embed.add_field(name='Antall kapitler lest', value=chapters_read)
            embed.add_field(name='Antall volum lest', value=volumes_read)
            embed.add_field(name='Antall manga lest', value=completed)
            embed.add_field(name='Leser nå', value=reading)
            embed.add_field(name='Planlegger å lese', value=f'{planning}\n({planning_days} kapitler)')
            embed.add_field(name='Droppet', value=dropped)
            if most_read_genres is not '':
                embed.add_field(name='Mest leste sjangere', value=most_read_genres, inline=False)
            if most_read_staff is not '':
                embed.add_field(name='Mest leste skapere', value=most_read_staff, inline=False)
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
                    description(asHtml: false)
                    episodes
                    duration
                    genres
                    isAdult
                    bannerImage
                    meanScore
                    coverImage {
                        large
                        color
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
                              f'Skriv `{self.bot.prefix}help {ctx.command}` for hjelp')

            nsfw = data['isAdult']
            if nsfw:
                return await Defaults.error_fatal_send(ctx, text='Animen du søkte på er NSFW. ' +
                                                                 'Gjør kommandoen i en NSFW-kanal isteden')

            cover_image = data['coverImage']['large']
            banner_image = data['bannerImage']
            mean_score = data['meanScore']

            color = data['coverImage']['color']
            if not color:
                color = 0x02A9FF
            else:
                color = color.replace('#', '0x')
                color = int(color, 0)

            title_romaji = data['title']['romaji']
            title_native = data['title']['native']
            title_english = data['title']['english']
            titles = [title_romaji, title_native, title_english]
            for i, title in enumerate(titles):
                if title is None:
                    titles[i] = ''
            title_romaji, title_native, title_english = titles

            description = data['description']
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

            embed = discord.Embed(color=color, title=title_romaji, url=url,
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
        """Viser informasjon om en manga"""

        async with ctx.channel.typing():

            query = '''
                query ($search: String) {
                    Media (search: $search, type: MANGA) {
                        siteUrl
                        format
                        status
                        description(asHtml: false)
                        volumes
                        chapters
                        genres
                        isAdult
                        bannerImage
                        meanScore
                        coverImage {
                            large
                            color
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
                              f'Skriv `{self.bot.prefix}help {ctx.command}` for hjelp')

            nsfw = data['isAdult']
            if nsfw:
                return await Defaults.error_fatal_send(ctx, text='Mangaen du søkte på er NSFW. ' +
                                                                 'Gjør kommandoen i en NSFW-kanal isteden')

            cover_image = data['coverImage']['large']
            banner_image = data['bannerImage']
            mean_score = data['meanScore']

            color = data['coverImage']['color']
            if not color:
                color = 0x02A9FF
            else:
                color = color.replace('#', '0x')
                color = int(color, 0)

            title_romaji = data['title']['romaji']
            title_native = data['title']['native']
            title_english = data['title']['english']
            titles = [title_romaji, title_native, title_english]
            for i, title in enumerate(titles):
                if title is None:
                    titles[i] = ''
            title_romaji, title_native, title_english = titles

            description = data['description']
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

            embed = discord.Embed(color=color, title=title_romaji, url=url,
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
