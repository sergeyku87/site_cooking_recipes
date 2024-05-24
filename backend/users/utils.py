from django.core.files.uploadedfile import InMemoryUploadedFile

import base64
import io
import re
import sys


def base64_to_image(data, name_image='default'):
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