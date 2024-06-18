from django.core.files.uploadedfile import InMemoryUploadedFile

from rest_framework import status
from rest_framework.response import Response
from collections import defaultdict
import base64
import io
import logging
import re
import sys

from api.utils.variables import (
    VALIDATION_MSG_NAME,
)


logger = logging.getLogger(__name__)
handler = logging.StreamHandler()
formatter = logging.Formatter(
    '%(name)s-%(asctime)s-%(levelname)s-%(message)s'
)

logger.setLevel(logging.DEBUG)
handler.setLevel(logging.DEBUG)
handler.setFormatter(formatter)
logger.addHandler(handler)


def short_name(name):
    if len(name) > 20:  # magic number
        name = name[:20]
        name = name.rstrip().split(' ')[:2]  # first two word
        return '-'.join(name)
    return name


def cyrilic_to_latinic(string):
    alphabet = {
        'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd',
        'е': 'e', 'ё': 'yo', 'ж': 'zh', 'з': 'z', 'и': 'i',
        'й': 'j', 'к': 'k', 'л': 'l', 'м': 'm', 'н': 'n',
        'о': 'o', 'п': 'p', 'р': 'r', 'с': 's', 'т': 't',
        'у': 'u', 'ф': 'f', 'х': 'kh', 'ц': 'ts', 'ч': 'ch',
        'ш': 'sh', 'щ': 'shch', 'ы': 'i', 'э': 'e', 'ю': 'yu',
        'я': 'ya'
    }
    result = ''
    for sign in string:
        if ord(sign) > 127:
            try:
                result += alphabet[sign.lower()]
            except KeyError:
                result += '-'
        else:
            result += sign
    return result


def base64_to_image(data, name_image='default'):
    """Convert image in format base64 in FILE IN MEMORY."""
    name_image = cyrilic_to_latinic(name_image)
    name_image = short_name(name_image)
    result = re.search(
        'data:image/(?P<ext>.*?);base64,(?P<code>.*)',
        data,
        re.DOTALL
    )
    if result:
        ext = result.groupdict().get('ext')
        code = result.groupdict().get('code')
    else:
        return 'Not correct'

    image_byte = base64.b64decode(code)
    io_bytes = io.BytesIO(image_byte)

    image = InMemoryUploadedFile(
        io_bytes,
        'ImageField',
        name_image + '.' + ext,
        ext.upper(),
        sys.getsizeof(io_bytes),
        None,
    )
    return image


def debug(func):
    """Decorator for input debug mesage in console."""

    def inner(*args, **kwargs):
        print('-' * 30)
        logger.debug(f'{func.__name__!r}')
        logger.debug(f'args: {func.__code__.co_varnames}')
        print()
        for name, arg in zip(func.__code__.co_varnames, args):
            logger.debug(name)
            logger.debug(arg)

        logger.debug(f'kwargs: {[kwarg for kwarg in kwargs]}')
        print('-' * 30)
        return func(*args, **kwargs)

    return inner


def representation_image(request, image_url):
    """Image save in db show how URL."""
    protocol = request.scheme
    domain = request.get_host()
    return f'{protocol}://{domain}{image_url}'


def delete_or_400(model, msg='Bad Request', *args, **kwargs):
    """
    Delete instance and return Response with status 204 or
    return Response with 400 status.
    """
    if model.objects.filter(*args, **kwargs).exists():
        model.objects.get(*args, **kwargs).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    return Response({'error': msg}, status=status.HTTP_400_BAD_REQUEST)


def validate_fields(sample, fields):
    for value in fields:
        if bool(re.search(sample, value)):
            return True, value
    return False, None


def collect_to_dict(queryset):
    collection = defaultdict(lambda: 0)
    for value in queryset:
        collection[
            (
                value.ingredient.name,
                value.ingredient.measurement_unit
            )
        ] += value.amount
    return dict(collection)


def specific_validate(data, handelr_err):
    result, value = validate_fields(
        '^me',
        [data.get('username'), data.get('first_name')]
    )
    if result:
        raise handelr_err(VALIDATION_MSG_NAME.format(value))
    return data
