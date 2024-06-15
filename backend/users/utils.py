import re


def validate_fields(sample, fields):
    for value in fields:
        if bool(re.search(sample, value)):
            return True, value
    return False, None
