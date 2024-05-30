from django.core.files.uploadedfile import InMemoryUploadedFile
from django.utils.text import slugify

import base64
import io
import logging
import re
import sys


logger = logging.getLogger(__name__)
handler = logging.StreamHandler()
formatter = logging.Formatter()

logger.setLevel(logging.DEBUG)
handler.setLevel(logging.DEBUG)
handler.setFormatter(formatter)
logger.addHandler(handler)

def short_name(name):
    if len(name) > 20: # magic number
        name = name[:20]
        name = name.rstrip().split(' ')[:2] # first two word
        return '-'.join(name)
    return name

def base64_to_image(data, name_image='default'):
    name_image = slugify(short_name(name_image))
    result = re.search(
        'data:image/(?P<ext>.*?);base64,(?P<code>.*)',
        data,
        re.DOTALL
    )
    if result:
        ext = result.groupdict().get('ext')
        code = result.groupdict().get('code')
    else:
        raise Exception(
            'Not correct string for extract code in base64 and format'
        )

    image_byte = base64.b64decode(code)
    io_bytes = io.BytesIO(image_byte)

    image = InMemoryUploadedFile(
        io_bytes,
        'ImageField',
        name_image + '.' + ext,
        ext.upper(),
        sys.getsizeof(io_bytes),
        None
    )
    return image

def debug(func):
    """Decorator for input debug mesage in console."""
    def inner(*args, **kwargs):
        print('-'*30)
        logger.debug(f'{func.__name__!r}')
        logger.debug(f'args: {func.__code__.co_varnames}')
        print()
        for name, arg in zip(func.__code__.co_varnames, args):
            logger.debug(name)
            logger.debug(arg)

        logger.debug(f'kwargs: {[kwarg for kwarg in kwargs]}')
        print('-'*30)
        return func(*args, **kwargs)
    return inner


