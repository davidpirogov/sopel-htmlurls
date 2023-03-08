import re
from typing import List

import validators

URL_REGEX = r"(?:www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b[-a-zA-Z0-9()@:%_\+.~#?&\/=\[\]]+"
"""
Finds anything resembling a URL
"""

URL_REGEX_HTTPS = r"https\:\/\/(?:www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b[-a-zA-Z0-9()@:%_\+.~#?&\/=\[\]]+"
"""
Only finds urls that begin with a http(s)
"""


def get_urls_from_string(input: str, find_https_only: bool = True) -> List[str]:
    """
    Gets all URLs from an input string and returns a list of valid. Note, it does not check
    the Urls for correctness

    :param input: The input string of text that can contain zero to many urls
    :param find_https_only: Flag which only matches http(s) urls
    """

    match_flags = re.UNICODE | re.MULTILINE | re.IGNORECASE

    if find_https_only:
        match_pattern = re.compile(URL_REGEX_HTTPS, flags=match_flags)
    else:
        match_pattern = re.compile(URL_REGEX, flags=match_flags)

    return re.findall(pattern=match_pattern, string=input)


def is_url_valid(url_input: str, allow_public_only: bool = True) -> bool:
    """
    Validates a urls, by default only permitting public urls

    :param url_input: The input url
    :param allow_public_only: Flag which permits only publically accessible urls to validate
    """

    validation_result = validators.url(url_input, public=allow_public_only)  # type: ignore

    if isinstance(validation_result, bool) and validation_result is True:
        return True

    return False
