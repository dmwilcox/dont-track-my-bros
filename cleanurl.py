#!/usr/bin/python

"""Extract an encoded URL from the parameters of a wrapping URL.

Pulls out an encoded URL such as a link embedded in tracking URL from
Facebook or Google.
"""

import urlparse


def is_url(maybe_url):
    """Check to see if a provided string is a full URL.

    Does not work with URLs w/o a protocol since urlparse module,
    can not not determine the hostname, which is fixable by doing
    a DNS query, if desired. TBD.
    """
    if isinstance(maybe_url, list):
        assert len(maybe_url) == 1
        maybe_url = maybe_url[0]

    url_pieces = urlparse.urlparse(maybe_url)
    if not all([url_pieces.scheme, url_pieces.netloc]):
        return False
    else:
        return True


def extract_url(url):
    """Pull out a URL from the encoded parameters of another URL.

    Assumes there is only 1 URL encoded in the parameters, the first
    by hash order is returned.  Also fixable by changing to a generator
    function and calling it more than once, needed? TBD.
    """
    query_str = urlparse.urlparse(url).query
    if query_str:
        query_data = urlparse.parse_qs(query_str)
        for key in query_data:
            if is_url(query_data[key]):
                # ugh, urlparse always seems to return lists, ugly
                return query_data[key][0]


if __name__ == '__main__':
    import sys
    if len(sys.argv) > 2:
        print 'Usage: %s "http://trackingurl.com?u=http%3A%2F%2Fwww.wanttogetto.com..."' % sys.argv[0]
        sys.exit(1)
    print extract_url(sys.argv[1])
