#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Extract an encoded URL from the parameters of a wrapping URL.

Pulls encoded URLs from links or text you provide. Share links with
your friends, not tracking cookies.

"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import argparse
import re
import sys

try:
    from urllib import parse as urlparse
except ImportError:
    import urlparse


# Matching is pretty strong ("protocol?://something" is the minimum).
# Extra excluded punctuation is used as a boundry to dig URLs out of
# encoded JSON and the like.
URL_REGEX = (r'([^:/#,"\'{}]+)://'  # matches protocol and ://
              '([^/?#,"\'{}]*)'     # domain
              '([^?#,"\'{}]*)'      # path up until '#' or '?'
              '(\?([^?,"\'{}]*))?'  # optionally a query string
              '(#([^\W]*))?')       # optionally an anchor
URL_REG = re.compile(URL_REGEX)


def get_urls(url):
    """Take a given URL or URL fragment and return any encoded URLs in it."""

    # Urlparse returns the whole string in 'query' when
    # nothing is recognized.
    query_str = urlparse.urlparse(url).query
    if query_str:
        query_data = urlparse.parse_qs(query_str)
        for key in query_data:
            q_value = query_data[key][0]
            # Scan values of URL form fields for 'URL shaped' strings here.
            for url_match in URL_REG.finditer(q_value):
                yield url_match.group()


def main(args, usage=''):
    for url in get_urls(args.url[0]):
        print(url)


def dispatch_main():
    parser = argparse.ArgumentParser(prog='cleanurl')
    parser.add_argument('url',
                        nargs=1,
                        help='Messy URL with embedded URLs -- surround with '
                             'single quotes.')
    args = parser.parse_args(sys.argv[1:])
    main(args, usage=parser.format_usage())


if __name__ == '__main__':
    dispatch_main()
