#!/usr/bin/python

"""Extract an encoded URL from the parameters of a wrapping URL.

Pulls out an encoded URLs from tracking links. Share the link with
your friend not the associated tracking cookies.

"""

import re
import urlparse


# Without enforcing some order ("http[s]?://something" is the minimum)
# the regex messes up; there are many match targets available.
# Extra punctuation is disallowed to handle things like encoded JSON in
# the URL.
URL_REGEX = (r'([^:/#,"\'{}]+)://'    # matches protocol and ://
                '([^/?#,"\'{}]*)'     # domain
                '([^?#,"\'{}]*)'      # path up until '#' or '?'
                '(\?([^?,"\'{}]*))?'  # optionally a query string
                '(#([^\W]*))?')       # optionally an anchor
URL_REG = re.compile(URL_REGEX)


def get_urls(url):
    """Take a given URL or URL fragment and return any encoded URLs in it."""
    # even if nothing is recognized the whole string is returned in 'query'
    # which is how query fragments are supported
    query_str = urlparse.urlparse(url).query
    if query_str:
        query_data = urlparse.parse_qs(query_str)
        for key in query_data:
            q_value = query_data[key][0]
            for url_match in URL_REG.finditer(q_value):
                yield url_match.group()


if __name__ == '__main__':
    import sys
    if len(sys.argv) > 2:
        print "Usage: %s 'https://goog-fb-adtrack.com/?url=http%3A%2F%2Fwww.youtube.com...'" % sys.argv[0]
        sys.exit(1)

    for url in get_urls(sys.argv[1]):
        print url
