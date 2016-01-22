#!/usr/bin/python

"""Extract an encoded URL from the parameters of a wrapping URL.

Pulls out an encoded URLs from tracking links. Share the link with
your friend not the associated tracking cookies.

"""

import re
import urlparse


# Thanks Uncle Berners-Lee (https://tools.ietf.org/html/rfc3986#appendix-B)
URL_REGEX = (r'(([^:/?#]+):)?'   # protocol, and protocol with ':'
              '(//([^/?#]*))?'   # //domain and domain
              '([^?#]*)'         # path
              '(\?([^#]*))?'     # query with and without leading '?'
              '(#(.*))?')        # anchor with and without leading '#'
URL_REG = re.compile(URL_REGEX)


# Without enforcing some order ("http[s]?://something" is the minimum)
# the regex messes up; there are many match targets available.
# Extra punctuation is disallowed to handle things like encoded JSON in
# the URL.
ORDER_REGEX = (r'([^:/#,"\'{}]+)://'  # matches protocol and ://
                '([^/?#,"\'{}]*)'     # domain
                '([^?#,"\'{}]*)'      # path up until '#' or '?'
                '(\?([^?,"\'{}]*))?'  # optionally a query string
                '(#([^\W]*))?')       # optionally an anchor
ORDER_REG = re.compile(ORDER_REGEX)


def url_encoding_table():
    """Return a dict mapping ascii characters to URL encoded characters.

    Why there isn't a forward 'quote' function in urlparse I don't know.
    """
    return dict([ (urlparse.unquote('%%%02x' % i), '%%%02x' % i)
                  for i in range(1 << 7) ])


def get_url(s):
    """Return an iterator of regex matches or None."""
    #match = URL_REG.search(s)
    #match = ORDER_REG.search(s)
    #if not match:
    #    return
    return ORDER_REG.finditer(s)


def get_urls(url):
    """Take the given URL or URL fragment and return any encoded URLs.

    Call get_url for every parameter value and yield any results
    they return.
    """
    # even if nothing is recognized the whole string is returned in 'query'
    # which is how query fragments are supported
    query_str = urlparse.urlparse(url).query
    if query_str:
        query_data = urlparse.parse_qs(query_str)
        for key in query_data:
            for url_match in ORDER_REG.finditer(query_data[key][0]):
                yield url_match.group()


if __name__ == '__main__':
    import sys
    if len(sys.argv) > 2:
        print "Usage: %s 'https://goog-fb-adtrack.com/?url=http%3A%2F%2Fwww.youtube.com...'" % sys.argv[0]
        sys.exit(1)

    for url in get_urls(sys.argv[1]):
        print url
