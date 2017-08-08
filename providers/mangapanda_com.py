#!/usr/bin/python3
# -*- coding: utf-8 -*-

from lxml.html import document_fromstring
import re
import json

# http://www.mangapanda.com/hunter-x-hunter
domainUri = 'http://www.mangapanda.com'
uriRegex = 'https?://(?:www.)?mangapanda.com/([^/]+)'


def test_url(url):
    test = re.match(uriRegex, url)
    if test is None:
        return False
    return len(test.groups()) > 0


def get_main_content(url, get=None, post=None):
    name = get_manga_name(url)
    url = '{}/{}'.format(domainUri, name)
    return get(url)


def get_volumes(content=None):
    parser = document_fromstring(content)
    result = parser.cssselect('#listing tr > td > a')
    if result is None:
        return []
    return [i.get('href') for i in result]


def get_archive_name(volume):
    result = re.search('/.+/([^/]+)', volume)
    name = result.groups()
    return name[0]


def _content2image_url(content):
    parser = document_fromstring(content)
    resutl = parser.cssselect('#imgholder img')
    return resutl[0].get('src')


def get_images(main_content=None, volume=None, get=None, post=None):
    _url = (domainUri + volume) if volume.find(domainUri) < 0 else volume

    content = get(_url)
    count_pages = document_fromstring(content)
    count_pages = count_pages.cssselect('#selectpage option')

    if count_pages is None:
        return []

    count_pages = len(count_pages)
    images = [_content2image_url(content)]

    n = 1
    while n < count_pages:
        content = get('{}/{}'.format(_url, n))
        images.append(_content2image_url(content))
        n += 1

    return images


def get_manga_name(url, get=None):
    result = re.match(uriRegex, url)
    if result is None:
        return ''
    result = result.groups()
    if not len(result):
        return ''
    return result[0]


if __name__ == '__main__':
    print('Don\'t run this, please!')