from requests import get
import urllib.request

from cogs.utils import Defaults


async def download_photo(ctx, link, max_file_size: int, meassurement_type: str, filepath: str):
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
            return await Defaults.error_fatal_send(ctx, text='Filen er for stor. Prøv et bilde som er mindre ' +
                                                             f'enn {max_file_size_actual} {meassurement}')

        try:
            await ctx.message.attachments[0].save(fp=filepath)
        except:
            await Defaults.error_fatal_send(ctx, text='Kunne ikke hente bilde!', mention=True)
            return False

    elif not ctx.message.attachments and link is not None:
        try:
            linked_file = get(str(link))
        except:
            await Defaults.error_fatal_send(ctx, text='Kunne ikke hente bilde!', mention=True)
            return False
        if len(linked_file.content) > max_file_size:
            await Defaults.error_fatal_send(ctx, text='Filen er for stor. Prøv et bilde som er mindre enn ' +
                                                      f'{max_file_size_actual} {meassurement}', mention=True)
            return False

        try:
            opener = urllib.request.build_opener()
            opener.addheaders = [('User-agent', 'Mozilla/5.0')]
            urllib.request.install_opener(opener)
            urllib.request.urlretrieve(link, filepath)
        except:
            await Defaults.error_fatal_send(ctx, text='Kunne ikke hente bilde!', mention=True)
            return False

    else:
        await Defaults.error_warning_send(ctx, text='Du må gi meg et bilde!', mention=True)
        return False

    return True


async def input_sanitizer(text):
    """Parses url parameters"""

    synonyms = {
        '&': '%26',
        '?': '%3F',
        '+': '%2B',
        ',': '%2C',
        '=': '%3D'
    }
    for key, value in synonyms.items():
        text = text.replace(key, value)

    return text


async def check_file_too_big(ctx, status_msg, file, max_file_size: int, meassurement_type: str):
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
