import secrets
import string

from django.utils.text import slugify

RANDOM_CHARS = string.digits + string.ascii_uppercase + string.ascii_lowercase

TRANSLIT_MAP = {
    'а': 'a',
    'б': 'b',
    'в': 'v',
    'г': 'g',
    'д': 'd',
    'е': 'e',
    'ё': 'yo',
    'ж': 'zh',
    'з': 'z',
    'и': 'i',
    'й': 'y',
    'к': 'k',
    'л': 'l',
    'м': 'm',
    'н': 'n',
    'о': 'o',
    'п': 'p',
    'р': 'r',
    'с': 's',
    'т': 't',
    'у': 'u',
    'ф': 'f',
    'х': 'kh',
    'ц': 'c',
    'ч': 'ch',
    'ш': 'sh',
    'щ': 'sch',
    'ъ': '',
    'ы': 'y',
    'ь': '',
    'э': 'e',
    'ю': 'yu',
    'я': 'ya',
}


def generate_code(length=6, allowed_chars=RANDOM_CHARS):
    return ''.join(secrets.choice(allowed_chars) for _ in range(length))


def translit(value):
    value = str(value).lower()

    if 'ый' in value:
        value = value.replace('ый', 'y')  # латинская y (вместо yy)

    transliterated_value = ''.join(TRANSLIT_MAP.get(i, i) for i in value)
    return slugify(transliterated_value)
