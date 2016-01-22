#!/usr/bin/python

"""Extract an encoded URL from the parameters of a wrapping URL.

Pulls encoded URLs from links or text you provide. Share links with
your friends, not tracking cookies.

"""

import re
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


if __name__ == '__main__':
    import sys
    if len(sys.argv) > 2:
        print ("Usage: %s '<messy url with encoded urls>"
               "\n\n'https://goog-fb-adtrack.com/?url=http%3A%2F%2Fwww.youtube.com...'" % sys.argv[0]
              )
        sys.exit(1)

    for url in get_urls(sys.argv[1]):
        print url
