from requests import get
import urllib.request
from codecs import open
from json import load as json_load
import pymongo

from ..utils import Defaults


async def download_photo(
        ctx, status_msg, link,
        max_file_size: int, meassurement_type: str, filepath: str):
    """Downloads photo from messsage and checks its filesize"""

    max_file_size_actual = max_file_size
    meassurement = meassurement_type
    meassurements = {
        "B": 1,
        "KB": 1000,
        "MB": 1000000,
        "GB": 1000000000
    }
    meassurement_type = meassurements[meassurement_type]
    max_file_size = max_file_size * meassurement_type

    if ctx.message.attachments != [] and not link:
        if ctx.message.attachments[0].size > max_file_size:
            return await Defaults.error_fatal_edit(
                ctx, status_msg,
                text='Filen er for stor. Prøv et bilde som er mindre enn ' +
                     f'{max_file_size_actual} {meassurement}')

        try:
            await ctx.message.attachments[0].save(fp=filepath)
        except:
            return await Defaults.error_fatal_edit(
                ctx, status_msg,
                text='Kunne ikke hente bilde!')

    elif not ctx.message.attachments and link is not None:
        try:
            linked_file = get(str(link))
        except:
            return await Defaults.error_fatal_edit(
                ctx, status_msg,
                text='Kunne ikke hente bilde!')
        if len(linked_file.content) > max_file_size:
            return await Defaults.error_fatal_edit(
                ctx, status_msg,
                text='Filen er for stor. Prøv et bilde som er mindre enn ' +
                     f'{max_file_size_actual} {meassurement}')

        try:
            urllib.request.urlretrieve(link, filepath)
        except:
            return await Defaults.error_fatal_edit(
                ctx, status_msg,
                text='Kunne ikke hente bilde!')

    else:
        return await Defaults.error_warning_edit(
            ctx, status_msg, text='Du må gi meg et bilde!')

    return True


async def check_file_too_big(ctx, status_msg, file,
                             max_file_size: int, meassurement_type: str):
    """Checks file size and send error message if True"""

    meassurement = meassurement_type
    max_file_size_actual = max_file_size
    meassurements = {
        "B": 1,
        "KB": 1000,
        "MB": 1000000,
        "GB": 1000000000
    }
    meassurement_type = meassurements[meassurement_type]

    max_file_size = max_file_size * meassurement_type

    if file > max_file_size:
        await Defaults.error_fatal_edit(
            ctx, status_msg,
            text='Filen er for stort. Prøv et bilde som er mindre enn ' +
                 f'mer enn {max_file_size_actual} {meassurement}')
        return True
    else:
        return False


async def default_db_insert(ctx):
    """Standardmal for ny bruker i database"""

    with open('config.json', 'r', encoding='utf8') as f:
        config = json_load(f)
        mongodb_url = config['mongodb_url']

    mongo = pymongo.MongoClient(mongodb_url)
    database = mongo['discord']
    database_col_users = database['users']

    database_col_users.insert_one(
        {'_id': ctx.author.id,
         'ordsky_consent': False,
         'ordsky_data': {f'{ctx.guild.id}': None}})
