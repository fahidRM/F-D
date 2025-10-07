import arrow
import re

from dateutil import parser


def is_uuid(val):
    return bool(re.compile(r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$').fullmatch(val))

def is_valid_name(name):
    return len(name) > 0 and bool(re.compile(r"^[A-Za-z .'-]+$").fullmatch(name))

def is_valid_email(email):
    return len(email) > 0 and re.match(re.compile(
        r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    ), email) is not None

def is_valid_instagram_handle(handle):
    if handle.startswith('@'):
        handle = handle[1:]
    else:
        return False
    return bool(re.compile(r'^(?!.*\.\.)(?!.*\.$)[A-Za-z0-9._]{1,30}$').fullmatch(handle))

def is_valid_tiktok_handle(handle):
    if handle.startswith('@'):
        handle = handle[1:]
    else:
        return False
    return bool(re.compile(r'^[a-zA-Z0-9._]{2,24}$').fullmatch(handle))


def is_valid_platform(platform):
    return platform in ['Instagram', 'TikTok', 'Facebook', 'Twitter', 'LinkedIn']


def format_date(date_str):
    date_format = "YYYY-MM-DD HH:mm:ss ZZ"
    return arrow.get(date_str).format(date_format)


def is_valid_date(date_str):
    try:
        parser.parse(date_str)
        return True
    except (ValueError, TypeError):
        return False

def is_valid_url(url):
    return re.match(re.compile(
            r'^(https?|ftps?)://'           # http(s) or ftp(s) protocol must be specified
            r'([a-zA-Z0-9.-]+|'            # domain... (alphanumeric, dashes, dots)
            r'\d{1,3}(?:\d\d{1,3}){3})'    # ...or IPv4 address
            r'(:\d+_)?'                    # optional port
            r'(/\S*)?$',                # optional path
            re.IGNORECASE
        ), url) is not None